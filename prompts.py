import class_school_info
import os
import streamlit as st
import openai
from openai import OpenAI

# Initialize the OpenAI client
openai_client = OpenAI()  # This creates the client that will be used for API calls

# def get_system_prompt(school_info):
def return_highlighted_text(school_info):
    return f"""
תן היילייט למנהל בית ספר בסגנון  "המדד שנמוך מהממוצע הוא{school_info.worst_anigma_name} _ , המדד נמוך ב___ אחוז מהממוצע הארצי . ההיגד המרכזי שבגללו המדד נמוך הוא ____":        
המדד שנמצא מתחת לממוצע {school_info.worst_anigma_name}
הפער מהממוצע הארצי: {school_info.worst_anigma_value*100} אחוזים
ההיגד שנמצא מתחת לממוצע: {school_info.worst_heg1_text}
  """
# ההיגד השני שנמצא מתחת לממוצע: {school_info.worst_heg2_text if hasattr(school_info, 'worst_heg2_text') else 'לא זמין'}
  
    
def return_prompt(school_info):#worst_anigma_name,worst_anigma_percent, worst_heg1_text,worst_heg2_text,best_anigma_name,best_anigma_percent):
    return f"""
### סיווג שאלות ###
כאשר אתה מקבל שאלה, עליך ראשית לסווג אותה לאחת מהקטגוריות הבאות:
1. שאלות על גרפים ונתונים
2. בקשה לדוח למנהל בית ספר
3. שאלות על חוזקות וחולשות של בית הספר
4. שאלות כלליות על התוכנית
5. שאלות הקשורות לקבצי מידע נוספים
6. בקשות להצגת גרפים

### הנחיות לפי סוג השאלה ###
כאשר המשתמש מבקש להציג גרפים או לראות את הנתונים בגרפים (קטגוריה 6), הצג את הגרפים הרלוונטיים בתוך הצ'אט. 
אם המשתמש כותב "הראה לי את הנתונים בגרפים" או בקשה דומה להצגת גרפים, השתמש בקוד הבא להצגת הגרפים:
```python
st.session_state.show_charts = {
    "risc": True,
    "ici": True,
    "spider": True,
    "summary": True
}
```
בנוסף, תן הסבר קצר על כל גרף והמשמעות שלו."""

def return_good_prompt(input, history):
  selected_school=st.session_state.graph_data["selected_school"]
  st.session_state.show_charts["summary"] = not st.session_state.show_charts["summary"]
                
  if st.session_state.show_charts["summary"]:
                    # יוצר הסבר משולב לכל הגרפים
                    combined_data = {
                        "school_name": selected_school,
                        "risc": st.session_state.graph_data.get("risc", {}),
                        "ici": st.session_state.graph_data.get("ici", {}),
                        "spider": st.session_state.graph_data.get("spider", {})
                    }
                    
                    summary_prompt = f"""
                    נתח את הנתונים הבאים של בית הספר {selected_school} ותן הסבר כולל על המשמעות שלהם:
                    
                    1. חוסן (RISC): 
                       ערך נוכחי: {st.session_state.graph_data.get('risc', {}).get('value', 'חסר')}
                       ממוצע ארצי: {st.session_state.graph_data.get('risc', {}).get('global_avg', 'חסר')}
                    
                    2. מיקוד שליטה פנימי (ICI):
                       ערך נוכחי: {st.session_state.graph_data.get('ici', {}).get('value', 'חסר')}
                       ממוצע ארצי: {st.session_state.graph_data.get('ici', {}).get('global_avg', 'חסר')}
                    
                    3. תפיסות זמן: [כאן נמצאים נתוני תפיסות הזמן השונות]
                    
                    שאלה או בקשה נוכחית מהמשתמש: {input}
                    
                    התייחס למשמעות המשולבת של כל המדדים והקשר ביניהם. התייחס גם לשאלה הספציפית של המשתמש אם רלוונטית. תן שאלות מנחות למנהל בית הספר שיעזרו לו לשפר את המצב.
                    """
                    
                    # מקום להצגת ההסבר המסכם בזמן אמת
                    summary_placeholder = st.empty()
                    
                    try:
                        # יצירת הודעות עם היסטוריית שיחה
                        messages = [
                            {
                                "role": "system", 
                                "content": """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
                                הסבר בבקשה את המשמעות המשולבת של כל המדדים הבאים עבור בית הספר והקשר ביניהם.
                                בהודעה הראשונה של השיחה תן סקירה על כל המדדים ותן שאלות לחשיבה. בנוסף הצע למנהל דברים נוספים שאתה יכול לעזור לו בהם. 
 
                                                                       
                                מדד החוסן (RISC) - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
                                
                                מיקוד שליטה פנימי (ICI) - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית חזקה יותר.
                                
                                תפיסות זמן - חמישה ממדים:
                                1. עבר שלילי - תפיסה שלילית של העבר, טראומות וחוויות קשות
                                2. עבר חיובי - תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים
                                3. הווה דטרמיניסטי - תפיסה פטליסטית של ההווה, חוסר שליטה
                                4. הווה הדוניסטי - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות
                                5. עתיד - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות
                                
                                סיים את ההסבר בשאלות מנחות למנהל בית הספר כגון:
                                'איך כיום בית הספר מעודד תלמידים להרגיש בעלות על המעשים שלהם?', 
                                'האם יש מקומות נוספים שהיית משלב יכולת לקחת בעלות על הצלחות או כשלונות ומידת ההשפעה האישית של התלמיד עליהן?'
                                """
                            }
                        ]
                        
                        # הוספת היסטוריית השיחה אם קיימת
                        if history:
                            for msg in history:
                                if msg["role"] in ["user", "assistant"]:
                                    messages.append({"role": msg["role"], "content": msg["content"]})
                        
                        # הוספת השאלה הנוכחית
                        messages.append({"role": "user", "content": summary_prompt})
                        
                        # קריאה למודל השפה לקבלת הסבר מסכם
                        response_stream = openai_client.chat.completions.create(
                            model="gpt-4o",
                            messages=messages,
                            temperature=0.5,
                            max_tokens=1500,
                            stream=True
                        )
                        
                        full_summary = ""
                        
                        # עדכון תוכן ההסבר בזמן קבלת תשובות מהמודל
                        for chunk in response_stream:
                            if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                                content = chunk.choices[0].delta.content
                                if content:
                                    full_summary += content
                                    summary_placeholder.markdown(full_summary + "▌")
                        
                        # תצוגה סופית של ההסבר המלא
                        summary_placeholder.markdown(full_summary)
                        
                        # שמירת ההסבר המסכם ב-session state
                        st.session_state.graph_explanations["summary"]["explanation"] = full_summary
                    
                    except Exception as e:
                        st.error(f"שגיאה בעת יצירת ההסבר המסכם: {str(e)}")
                        summary_placeholder.markdown("לא ניתן ליצור הסבר מסכם כרגע. אנא נסה שוב מאוחר יותר.")

                    st.write(full_summary)
                    return full_summary
# Function to handle displaying graphs in chat when requested
def display_charts_in_chat():
    """
    Display the graphs directly in the chat area when requested by the user
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### מדד חוסן")
        if st.session_state.graph_data["risc"] is not None:
            from graph_manager import Gauge_Graph_type
            import draw_gauge
            
            risc_value = st.session_state.graph_data["risc"]["value"]
            risc_global = st.session_state.graph_data["risc"]["global_avg"]
            
            # Create and display RISC graph
            fig_risc = draw_gauge.draw_gauge("חוסן", risc_value, risc_global, "ממוצע ארצי")
            st.plotly_chart(fig_risc, use_container_width=True)
    
    with col2:
        st.markdown("### מיקוד שליטה פנימי (ICI)")
        if st.session_state.graph_data["ici"] is not None:
            from graph_manager import Gauge_Graph_type
            import draw_gauge
            
            ici_value = st.session_state.graph_data["ici"]["value"]
            ici_global = st.session_state.graph_data["ici"]["global_avg"]
            
            # Create and display ICI graph
            fig_ici = draw_gauge.draw_gauge("מיקוד שליטה פנימי", ici_value, ici_global, "ממוצע ארצי")
            st.plotly_chart(fig_ici, use_container_width=True)
    
    with col3:
        st.markdown("### תפיסות זמן")
        if st.session_state.graph_data["spider"] is not None:
            import draw_spider_graph
            import plotly.graph_objects as go
            
            # Create spider chart based on available data
            if "negetive_past" in st.session_state.graph_data["spider"]:
                # Old format
                categories = ["עבר שלילי", "עבר חיובי", "הווה דטרמיניסטי", 
                             "הווה הדוניסטי", "עתיד"]
                
                current_values = [
                    st.session_state.graph_data["spider"]["negetive_past"]["current"],
                    st.session_state.graph_data["spider"]["positive_past"]["current"],
                    st.session_state.graph_data["spider"]["fatalic_present"]["current"],
                    st.session_state.graph_data["spider"]["hedonistic_present"]["current"],
                    st.session_state.graph_data["spider"]["future"]["current"]
                ]
                
                global_values = [
                    st.session_state.graph_data["spider"]["negetive_past"]["global"],
                    st.session_state.graph_data["spider"]["positive_past"]["global"],
                    st.session_state.graph_data["spider"]["fatalic_present"]["global"],
                    st.session_state.graph_data["spider"]["hedonistic_present"]["global"],
                    st.session_state.graph_data["spider"]["future"]["global"]
                ]
            else:
                # New format with future_ prefix
                categories = ["עבר שלילי", "עבר חיובי", "הווה דטרמיניסטי", 
                             "הווה הדוניסטי", "עתיד"]
                
                current_values = [
                    st.session_state.graph_data["spider"]["future_negetive_past"]["current"],
                    st.session_state.graph_data["spider"]["future_positive_past"]["current"],
                    st.session_state.graph_data["spider"]["future_fatalic_present"]["current"],
                    st.session_state.graph_data["spider"]["future_hedonistic_present"]["current"],
                    st.session_state.graph_data["spider"]["future_future"]["current"]
                ]
                
                global_values = [
                    st.session_state.graph_data["spider"]["future_negetive_past"]["global"],
                    st.session_state.graph_data["spider"]["future_positive_past"]["global"],
                    st.session_state.graph_data["spider"]["future_fatalic_present"]["global"],
                    st.session_state.graph_data["spider"]["future_hedonistic_present"]["global"],
                    st.session_state.graph_data["spider"]["future_future"]["global"]
                ]
            
            fig = go.Figure()
            
            # Current values
            fig.add_trace(go.Scatterpolar(
                r=current_values,
                theta=categories,
                fill='none',
                name='ממוצע נוכחי',
                line=dict(color='#437742')
            ))
            
            # Global average
            fig.add_trace(go.Scatterpolar(
                r=global_values,
                theta=categories,
                fill='none',
                name='ממוצע ארצי',
                line=dict(color='#1F3B91')
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[1, 5]
                    )
                ),
                showlegend=True,
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Add an explanation for the graphs
    st.markdown("""
    ### הסבר הגרפים
    
    **מדד החוסן (RISC)** - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
    
    **מיקוד שליטה פנימי (ICI)** - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית חזקה יותר.
    
    **תפיסות זמן** - מציג חמישה ממדים של תפיסת זמן:
    1. עבר שלילי - תפיסה שלילית של העבר, טראומות וחוויות קשות
    2. עבר חיובי - תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים
    3. הווה דטרמיניסטי - תפיסה פטליסטית של ההווה, חוסר שליטה
    4. הווה הדוניסטי - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות
    5. עתיד - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות
    """)
