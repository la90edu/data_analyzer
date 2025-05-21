import streamlit as st
import pandas as pd
from class_school_info import SchoolInfo
import init
import llms  # הוספת ייבוא למודול llms
import os
from openai import OpenAI
from dotenv import load_dotenv

# טעינת משתני הסביבה מקובץ .env
load_dotenv()

# קבלת ה-API key מהמשתנים והגדרת הלקוח
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai_client = OpenAI(api_key=api_key)
else:
    openai_client = OpenAI()  # יתכן שיעבוד אם יש API key בסביבה

# טעינת הנתונים - init כבר כולל את set_page_config לכן אין צורך לקרוא לה שוב
try:
    df = init.init()
except Exception as e:
    st.error(f"שגיאה בטעינת הנתונים: {e}")
    df = pd.DataFrame()

# יצירת משתנה session state לשמירת מצב הצגת הגרפים
if "show_graphs_state" not in st.session_state:
    st.session_state.show_graphs_state = False

# הוספת תמיכה ב-RTL ועיצוב מותאם
st.markdown("""
<style>
/* תמיכה ב-RTL */
h1, h2, h3, h4, h5, h6, p, div {
    text-align: right;
    direction: rtl;
}

/* עיצוב בחירת בית ספר בראש העמוד */
.school-selector {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    text-align: center;
}

/* עיצוב תיבת הבחירה */
div[data-testid="stSelectbox"] {
    text-align: right;
    direction: rtl;
    max-width: 400px;
    margin: 0 auto;
}

/* עיצוב הגרפים */
.stPlotlyChart {
    background-color: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

/* עיצוב כרטיס הסבר */
.explanation-box {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# כותרת הדף
st.title("דאשבורד ניתוח נתונים 📊")

# אזור בחירת בית הספר בראש העמוד
st.markdown('<div class="school-selector">', unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom: 15px;'>בחר בית ספר לניתוח</h3>", unsafe_allow_html=True)

if not df.empty and 'school' in df.columns:
    unique_schools = df["school"].unique().tolist()
    selected_school = st.selectbox("בחר בית ספר:", unique_schools, key="school_selector")
    filtered_df = df[df['school'] == selected_school] if selected_school else df
else:
    st.warning("לא נמצאו נתונים לסינון")
    filtered_df = df

st.markdown('</div>', unsafe_allow_html=True)


# יצירת משתני מצב אם לא קיימים
if "graph_data" not in st.session_state:
    st.session_state.graph_data = {
        "risc": None,
        "ici": None, 
        "spider": None,
        "selected_school": None
    }

# יצירת משתני מצב להסברים אם לא קיימים
if "explanations" not in st.session_state:
    st.session_state.explanations = {
        "risc": "",
        "ici": "",
        "spider": "",
        "combined": "",
        "research": "",  # הוספת משתנה להסבר על המחקר
        "metrics": ""    # הוספת משתנה להסבר על המדדים
    }

# יצירת משתני מצב להצגת הסברים
if "show_explanations" not in st.session_state:
    st.session_state.show_explanations = {
        "risc": False,
        "ici": False,
        "spider": False,
        "combined": False,
        "research": False,  # הוספת משתנה להצגת הסבר על המחקר
        "metrics": False    # הוספת משתנה להצגת הסבר על המדדים
    }

if selected_school and not filtered_df.empty:
    # יצירת אובייקט SchoolInfo
    school_info = SchoolInfo(filtered_df)
    
    #אתחול גרפים 
    fig_risc = school_info.get_fig_risc("חוסן")
    fig_ici = school_info.get_fig_ici("מיקוד שליטה")
    fig_spider = school_info.get_fig_spider()
    
    st.session_state.graph_data["risc"] = {
            "value": school_info.risc,
            "global_avg": st.session_state.global_average["risc"],
            "research_avg": st.session_state.research_average["risc"]
        }
    st.session_state.graph_data["ici"] = {
            "value": school_info.ici,
            "global_avg": st.session_state.global_average["ici"],
            "research_avg": st.session_state.research_average["ici"]
        }
    st.session_state.graph_data["spider"] = {
            "future_negetive_past": {
                "current": school_info.future_negetive_past,
                "global": st.session_state.global_average["future_negetive_past"],
                "research": st.session_state.research_average["future_negetive_past"]
            },
            "future_positive_past": {
                "current": school_info.future_positive_past,
                "global": st.session_state.global_average["future_positive_past"],
                "research": st.session_state.research_average["future_positive_past"]
            },
            "future_fatalic_present": {
                "current": school_info.future_fatalic_present,
                "global": st.session_state.global_average["future_fatalic_present"],
                "research": st.session_state.research_average["future_fatalic_present"]
            },
            "future_hedonistic_present": {
                "current": school_info.future_hedonistic_present,
                "global": st.session_state.global_average["future_hedonistic_present"],
                "research": st.session_state.research_average["future_hedonistic_present"]
            },
            "future_future": {
                "current": school_info.future_future,
                "global": st.session_state.global_average["future_future"],
                "research": st.session_state.research_average["future_future"]
            }
        }
    # 
    # 
    # 
    
    # כפתור להראות ניתוח מקיף
    if st.button("הראה לי ניתוח מקיף", key="show_combined_explanation"):
            st.session_state.show_explanations["combined"] = not st.session_state.show_explanations["combined"]
            
            # אם צריך להציג הסבר מסכם וההסבר ריק - קבל הסבר חדש
            if st.session_state.show_explanations["combined"] and not st.session_state.explanations["combined"]:
                combined_placeholder = st.empty()
                combined_placeholder.markdown("מייצר ניתוח מקיף...")
                
                # יצירת פרומפט מסכם לכל הגרפים
                summary_prompt = f"""
                נתח את הנתונים הבאים של בית הספר {selected_school} ותן הסבר כולל על המשמעות שלהם:
                
                1. חוסן (RISC): 
                   ערך נוכחי: {st.session_state.graph_data.get('risc', {}).get('value', 'חסר')}
                   ממוצע ארצי: {st.session_state.graph_data.get('risc', {}).get('global_avg', 'חסר')}
                
                2. מיקוד שליטה פנימי (ICI):
                   ערך נוכחי: {st.session_state.graph_data.get('ici', {}).get('value', 'חסר')}
                   ממוצע ארצי: {st.session_state.graph_data.get('ici', {}).get('global_avg', 'חסר')}
                
                3. תפיסות זמן: [נתוני תפיסות הזמן השונות]
                
                התייחס למשמעות המשולבת של כל המדדים והקשר ביניהם. תן שאלות מנחות למנהל בית הספר שיעזרו לו לשפר את המצב.
                """
                
                # מערכת פרומפט לניתוח מסכם
                system_prompt = """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
                הסבר בבקשה את המשמעות המשולבת של כל המדדים הבאים עבור בית הספר והקשר ביניהם.
                
                מדד החוסן (RISC) - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
                
                מיקוד שליטה פנימי (ICI) - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית חזקה יותר.
                
                תפיסות זמן - חמישה ממדים:
                1. עבר שלילי - תפיסה שלילית של העבר, טראומות וחוויות קשות
                2. עבר חיובי - תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים
                3. הווה דטרמיניסטי - תפיסה פטליסטית של ההווה, חוסר שליטה
                4. הווה הדוניסטי - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות
                5. עתיד - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות
                
                סיים את ההסבר בשאלות מנחות למנהל בית הספר שיכולות לעודד אותו לחשוב על שיפור המצב שלו.
                לדוגמה: 'איך כיום בית הספר מעודד תלמידים להרגיש בעלות על המעשים שלהם?', 'האם יש מקומות נוספים שהיית משלב יכולת לקחת בעלות על הצלחות או כשלונות ומידת ההשפעה האישית של התלמיד עליהן?'
                """
                
                try:
                    # קריאה למודל השפה לקבלת הסבר מסכם
                    response_stream = openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": summary_prompt}
                        ],
                        temperature=0.5,
                        max_tokens=1500,
                        stream=True
                    )
                    
                    full_explanation = ""
                    
                    # עדכון תוכן ההסבר בזמן קבלת תשובות מהמודל
                    for chunk in response_stream:
                        if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                            content = chunk.choices[0].delta.content
                            if content:
                                full_explanation += content
                                combined_placeholder.markdown(full_explanation + "▌")
                    
                    # תצוגה סופית של ההסבר המלא
                    combined_placeholder.markdown(full_explanation)
                    
                    # שמירת ההסבר המסכם
                    st.session_state.explanations["combined"] = full_explanation
                    
                except Exception as e:
                    error_msg = f"לא הצלחנו לייצר ניתוח מקיף. שגיאה: {str(e)}"
                    combined_placeholder.error(error_msg)
                    st.session_state.explanations["combined"] = error_msg
    
    # הוספת כפתור להצגת המלצות שיפור ספציפיות
    if st.button("במה הכי כדאי לי להשתפר", key="improvement_recommendation"):
        # יצירת משתנה מצב להמלצות שיפור אם לא קיים
        if "improvement_recommendation" not in st.session_state.explanations:
            st.session_state.explanations["improvement_recommendation"] = ""
        
        improvement_placeholder = st.empty()
        improvement_placeholder.markdown("מייצר המלצות שיפור מותאמות אישית...")
        
        # יצירת פרומפט להמלצות שיפור
        improvement_prompt = f"""
        בתור יועץ חינוכי, הכן המלצה מפורטת ומנומקת למנהל בית הספר {selected_school} על סמך הנתונים הבאים:
        
        המדד החלש ביותר בבית הספר הוא: {school_info.worst_anigma_name}
        ההיגד הבעייתי ביותר במדד זה הוא: {school_info.worst_heg1_text}
        
        כתוב המלצה מפורטת, מנומסת ומנומקת למנהל, תוך התייחסות ספציפית למדד החלש ולהיגד הבעייתי.
        תן דוגמאות קונקרטיות לפעולות שהמנהל יכול לבצע כדי לשפר את המדד הספציפי הזה.
        """
        
        # מערכת פרומפט להמלצות שיפור
        improvement_system_prompt = """
        אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים ובית ספר. 
        
        בהמלצה שלך, התייחס לנקודות הבאות:
        1. תן הסבר ברור וידידותי על המדד החלש ומשמעותו בהקשר החינוכי
        2. הסבר את ההשלכות של המדד החלש על התלמידים והסביבה הלימודית
        3. תן כמה שאלות לחשיבה למנהל שיכולות לגרום לו להבין מה קורה אצלו בבית הספר ואיך אפשר לשפר את המצב       
        
        אל תתן המלצות ואל תסכם את השיחה .   
        """
        
        try:
            # קריאה למודל השפה לקבלת המלצות שיפור
            response_stream = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": improvement_system_prompt},
                    {"role": "user", "content": improvement_prompt}
                ],
                temperature=0.5,
                max_tokens=1500,
                stream=True
            )
            
            full_recommendation = ""
            
            # עדכון תוכן ההמלצות בזמן קבלת תשובות מהמודל
            for chunk in response_stream:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                    content = chunk.choices[0].delta.content
                    if content:
                        full_recommendation += content
                        improvement_placeholder.markdown(full_recommendation + "▌")
            
            # תצוגה סופית של ההמלצות המלאות בתוך מסגרת מעוצבת
            improvement_placeholder.markdown(f"""
            <div class="explanation-box">
                <h3>המלצות לשיפור בית הספר</h3>
                {full_recommendation}
            </div>
            """, unsafe_allow_html=True)
            
            # שמירת ההמלצות
            st.session_state.explanations["improvement_recommendation"] = full_recommendation
            
        except Exception as e:
            error_msg = f"לא הצלחנו לייצר המלצות שיפור. שגיאה: {str(e)}"
            improvement_placeholder.error(error_msg)
            st.session_state.explanations["improvement_recommendation"] = error_msg
                  
    
# הוספת כפתור "אני רוצה הסבר על המחקר", פונקציה והצגת תוכן ההסבר
if st.button("אני רוצה הסבר על המחקר", key="research_explanation_button"):
    st.session_state.show_explanations["research"] = True
    
    # אם צריך להציג הסבר על המחקר וההסבר ריק - קבל הסבר חדש
    if st.session_state.show_explanations["research"] and not st.session_state.explanations["research"]:
        research_placeholder = st.empty()
        research_placeholder.markdown("מייצר הסבר על המחקר...")
        
        # מידע על המחקר
        research_info = """
        מטרת הציר המנטלי בתוכנית ההיי טק היא לפתח דפוס חשיבה מתפתח אשר יתרום משמעותית לקידום
        תלמידי חטיבות ביניים ותיכונים מהפריפריה (מדד טיפוח 6-10) לקריירות היי-טק בישראל. התוכנית היא
        בעלת גישה הוליסטית, הכוללת לא רק תלמידים אלא גם הכשרת אנשי חינוך כסוכני שינוי ומערבת את
        המנהיגות הבית ספרית בתהליך על מנת ליצור מיקסום האימפקט של התוכנית. לצד סדנאות לפיתוח דפוס
        חשיבה מתפתח, התוכנית משלבת חוויה יזמית מעשית עם פיתוח דפוס חשיבה מתפתח. התלמידים
        משתתפים בפעילויות ותחרויות דמויות סטארטאפ תוך שהם לומדים שניתן לפתח את היכולות שלהם
        באמצעות מסירות ועבודה קשה. התוכנית מלווה על ידי חברות טכנולוגיה שונות כמו גוגל, מיקרוסופט, אמזון
        ואינטל, יחד עם שותפים במגזר החינוכי והציבורי.
        חזון התוכנית
        יצירת תמונת עתיד של מרחב הזדמנויות עתידיות בהייטק ופיתוח גישות חיוביות כלפי למידה והתפתחות
        אישית (כולל ביטחון עצמי, תחושת מסוגלות, חוסן ומוטיבציה להיכנס להייטק).
        קהל היעד
        תלמידים בכיתות ח' ו-י' ב-93 בתי ספר במדדי טיפוח 6-10
        """
        
        # יצירת פרומפט להסבר על המחקר
        if selected_school:
            school_context = f"""
            נתוני בית הספר {selected_school}:
            
            1. חוסן (RISC): 
            ערך נוכחי: {st.session_state.graph_data.get('risc', {}).get('value', 'חסר')}
            ממוצע ארצי: {st.session_state.graph_data.get('risc', {}).get('global_avg', 'חסר')}
            
            2. מיקוד שליטה פנימי (ICI):
            ערך נוכחי: {st.session_state.graph_data.get('ici', {}).get('value', 'חסר')}
            ממוצע ארצי: {st.session_state.graph_data.get('ici', {}).get('global_avg', 'חסר')}
            """
        else:
            school_context = "אין נתונים זמינים לבית ספר ספציפי כרגע."
            
        # מערכת פרומפט להסבר המחקר
        system_prompt = """
        אתה מומחה חינוכי המסביר מחקרים פסיכולוגיים וחינוכיים. 
        
        הסבר את המחקר באופן תמציתי ונחמד, תוך התייחסות לנקודות הבאות:
        1. מטרות המחקר והרקע לו
        2. הגישה החינוכית והפסיכולוגית (כולל דפוס חשיבה מתפתח)
        3. הקשר בין המדדים הנמדדים (חוסן, מיקוד שליטה פנימי, תפיסות זמן) ובין הצלחה בלימודים ובתחום ההייטק
        4. משמעות הנתונים עבור בית הספר הספציפי (אם יש)
        
        הסבר את המידע בצורה ידידותית, מקצועית ומכבדת. התאם את ההסבר למנהלים ואנשי חינוך.
ללא לסכם את השיחה ולא לאחל בהצלחה או בברכה . 
"""
        
        research_prompt = f"""
        הסבר בבקשה את המחקר הבא בהקשר של בית הספר ומדדי החוסן, מיקוד השליטה הפנימי ותפיסות הזמן:
        
        {research_info}
        
        {school_context}
        
        בהסבר שלך, התייחס לחשיבות של מדדי החוסן, מיקוד השליטה הפנימי ותפיסות הזמן בהקשר של התוכנית,
        וכיצד הם משפיעים על הצלחה אקדמית ומקצועית בתחום ההייטק.
        """
        
        try:
            # קריאה למודל השפה לקבלת הסבר על המחקר
            response_stream = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": research_prompt}
                ],
                temperature=0.5,
                max_tokens=1500,
                stream=True
            )
            
            full_explanation = ""
            
            # עדכון תוכן ההסבר בזמן קבלת תשובות מהמודל
            for chunk in response_stream:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                    content = chunk.choices[0].delta.content
                    if content:
                        full_explanation += content
                        research_placeholder.markdown(full_explanation + "▌")
            
            # תצוגה סופית של ההסבר המלא בתוך מסגרת
            research_placeholder.markdown(f"""
            <div class="explanation-box">
                <h3>הסבר על המחקר</h3>
                {full_explanation}
            </div>
            """, unsafe_allow_html=True)
            
            # שמירת ההסבר על המחקר
            st.session_state.explanations["research"] = full_explanation
            
        except Exception as e:
            error_msg = f"לא הצלחנו לייצר הסבר על המחקר. שגיאה: {str(e)}"
            research_placeholder.error(error_msg)
            st.session_state.explanations["research"] = error_msg
    else:
        # הצגת ההסבר השמור
        st.markdown(f"""
        <div class="explanation-box">
            <h3>הסבר על המחקר</h3>
            {st.session_state.explanations["research"]}
        </div>
        """, unsafe_allow_html=True)
             

    
    
    
    # 
    # 
    # 
    # גת הגרפים בטורים
    # בדיקה אם יש לחיצה על כפתור הצגת גרפים או אם הגרפים כבר הוצגו קודם
if st.button("הצג לי גרפים") or st.session_state.show_graphs_state:
        # עדכון המצב לזכור שהגרפים הוצגו
        st.session_state.show_graphs_state = True
        
        st.markdown("### מדד חוסן")
        fig_risc = school_info.get_fig_risc("חוסן")
        st.plotly_chart(fig_risc, use_container_width=True)
        
        # שמירת נתוני גרף חוסן למצב
        st.session_state.graph_data["risc"] = {
            "value": school_info.risc,
            "global_avg": st.session_state.global_average["risc"],
            "research_avg": st.session_state.research_average["risc"]
        }
        
        
        st.markdown("### מיקוד שליטה פנימי")
        fig_ici = school_info.get_fig_ici("מיקוד שליטה")
        st.plotly_chart(fig_ici, use_container_width=True)
        
        # שמירת נתוני גרף מיקוד שליטה למצב
        st.session_state.graph_data["ici"] = {
            "value": school_info.ici,
            "global_avg": st.session_state.global_average["ici"],
            "research_avg": st.session_state.research_average["ici"]
        }
        
        
        st.markdown("### התפלגות לפי ממדי זמן")
        fig_spider = school_info.get_fig_spider()
        st.plotly_chart(fig_spider, use_container_width=True)
        
        # שמירת נתוני גרף עכביש למצב
        anigmas_dict = school_info.return_anigmas_result_as_dict()
        st.session_state.graph_data["spider"] = {
            "future_negetive_past": {
                "current": anigmas_dict["future_negetive_past"],
                "global": st.session_state.global_average["future_negetive_past"],
                "research": st.session_state.research_average["future_negetive_past"]
            },
            "future_positive_past": {
                "current": anigmas_dict["future_positive_past"],
                "global": st.session_state.global_average["future_positive_past"],
                "research": st.session_state.research_average["future_positive_past"]
            },
            "future_fatalic_present": {
                "current": anigmas_dict["future_fatalic_present"],
                "global": st.session_state.global_average["future_fatalic_present"],
                "research": st.session_state.research_average["future_fatalic_present"]
            },
            "future_hedonistic_present": {
                "current": anigmas_dict["future_hedonistic_present"],
                "global": st.session_state.global_average["future_hedonistic_present"],
                "research": st.session_state.research_average["future_hedonistic_present"]
            },
            "future_future": {
                "current": anigmas_dict["future_future"],
                "global": st.session_state.global_average["future_future"],
                "research": st.session_state.research_average["future_future"]
            }
        }
        
# הוספת כפתור "הסבר לי עוד על המדדים"
if st.button("הסבר לי עוד על המדדים"):
    st.session_state.show_explanations["metrics"] = True
    
    # אם צריך להציג הסבר על המדדים וההסבר ריק - קבל הסבר חדש
    if st.session_state.show_explanations["metrics"] and not st.session_state.explanations["metrics"]:
        metrics_placeholder = st.empty()
        metrics_placeholder.markdown("מייצר הסבר על המדדים...")
        
        # יצירת פרומפט להסבר על המדדים
        metrics_prompt = f"""
        הסבר את המדדים הבאים בהקשר של נתוני בית הספר {selected_school}:
        
        1. חוסן (RISC): 
           ערך נוכחי: {st.session_state.graph_data.get('risc', {}).get('value', 'חסר')}
           ממוצע ארצי: {st.session_state.graph_data.get('risc', {}).get('global_avg', 'חסר')}
        
        2. מיקוד שליטה פנימי (ICI):
           ערך נוכחי: {st.session_state.graph_data.get('ici', {}).get('value', 'חסר')}
           ממוצע ארצי: {st.session_state.graph_data.get('ici', {}).get('global_avg', 'חסר')}
        
        3. תפיסות זמן: [נתוני תפיסות הזמן השונות]
        
        הסבר את המשמעות של כל מדד וכיצד הוא רלוונטי לנתוני בית הספר. תן דוגמאות מעשיות לשימוש במדדים אלה לשיפור המצב בבית הספר.
        """
        
        # מערכת פרומפט להסבר על המדדים
        system_prompt = """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
        הסבר בבקשה את המשמעות של המדדים הבאים עבור בית הספר:
        
        מדד החוסן (RISC) - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
        
        מיקוד שליטה פנימי (ICI) - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית חזקה יותר.
        
        תפיסות זמן - חמישה ממדים:
        1. עבר שלילי - תפיסה שלילית של העבר, טראומות וחוויות קשות
        2. עבר חיובי - תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים
        3. הווה דטרמיניסטי - תפיסה פטליסטית של ההווה, חוסר שליטה
        4. הווה הדוניסטי - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות
        5. עתיד - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות
        
        הסבר את המדדים בצורה ברורה ומעמיקה, תוך מתן דוגמאות מעשיות לשימוש בהם.
        """
        
        try:
            # קריאה למודל השפה לקבלת הסבר על המדדים
            response_stream = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": metrics_prompt}
                ],
                temperature=0.5,
                max_tokens=1500,
                stream=True
            )
            
            full_explanation = ""
            
            # עדכון תוכן ההסבר בזמן קבלת תשובות מהמודל
            for chunk in response_stream:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                    content = chunk.choices[0].delta.content
                    if content:
                        full_explanation += content
                        metrics_placeholder.markdown(full_explanation + "▌")
            
            # תצוגה סופית של ההסבר המלא
            metrics_placeholder.markdown(full_explanation)
            
            # שמירת ההסבר על המדדים
            st.session_state.explanations["metrics"] = full_explanation
            
        except Exception as e:
            error_msg = f"לא הצלחנו לייצר הסבר על המדדים. שגיאה: {str(e)}"
            metrics_placeholder.error(error_msg)
            st.session_state.explanations["metrics"] = error_msg
    else:
        # הצגת ההסבר השמור
        st.markdown(f"""
        <div class="explanation-box">
            <h3>הסבר על המדדים</h3>
            {st.session_state.explanations["metrics"]}
        </div>
        """, unsafe_allow_html=True)

