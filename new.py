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
# st.title("דאשבורד ניתוח נתונים 📊")

# הוספת הסבר על הדאשבורד
st.markdown("""
<div class="explanation-box" style="margin-bottom: 30px;">
    <h3>ברוכים הבאים לדאשבורד הנתונים</h3>
    <p>מנהל/ת יקר/ה, לאחרונה השתתפו תלמידי בית הספר שלך בתכנית "הציר המנטלי" שמטרתה לבחון תפיסות עצמיות של תלמידים בהיבטים מרכזיים בחייהם - כמו היכולת להתמודד עם אתגרים, מניעים לקבלת ההחלטות שלהם לטווח הרחוק, גמישות שלהם לסביבה משתנה ותפיסתם לגבי השפעתם על העתיד שלהם. למטה מובואות כמה מסקנות מהנתונים לגבי בית הספר שלך.</p>
</div>
""", unsafe_allow_html=True)
# אזור בחירת בית הספר בראש העמוד
# st.markdown('<div class="school-selector">', unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom: 15px;'>בחר/י בית ספר לניתוח</h3>", unsafe_allow_html=True)

if not df.empty and 'school' in df.columns:
    unique_schools = df["school"].unique().tolist()
    selected_school = st.selectbox("בחר בית ספר:", unique_schools, key="school_selector")
    filtered_df = df[df['school'] == selected_school] if selected_school else df
else:
    st.warning("לא נמצאו נתונים לסינון")
    filtered_df = df

st.markdown('</div>', unsafe_allow_html=True)


#יצירת סיכום שיסתמכך על התוצאות שמתקבלות מ SchoolInfo.return_text_from_round_delta(ici),school_info.return_text_from_round_delta(risc) ,school_info.return_text_from_round_delta(future_negetive_past),school_info.return_text_from_round_delta(future_positive_past),school_info.return_text_from_round_delta(future_fatalic_present),school_info.return_text_from_round_delta(future_hedonistic_present),school_info.return_text_from_round_delta(future_future)

# הוספת כפתור ליצירת סיכום באמצעות מודל שפה
if selected_school and not filtered_df.empty:
    # יצירת אובייקט SchoolInfo לחישוב הנתונים (אם לא קיים כבר)
    if 'school_info_summary' not in locals():
        school_info_summary = SchoolInfo(filtered_df)
    
    # קבלת טקסט המתאר את מצב בית הספר בכל מדד ביחס לממוצע הארצי
    ici_text = school_info_summary.return_text_from_round_delta("ici")
    risc_text = school_info_summary.return_text_from_round_delta("risc")
    future_negetive_past_text = school_info_summary.return_text_from_round_delta("future_negetive_past")
    future_positive_past_text = school_info_summary.return_text_from_round_delta("future_positive_past")
    future_fatalic_present_text = school_info_summary.return_text_from_round_delta("future_fatalic_present")
    future_hedonistic_present_text = school_info_summary.return_text_from_round_delta("future_hedonistic_present")
    future_future_text = school_info_summary.return_text_from_round_delta("future_future")
    
    # הצגת סיכום המדדים לפני כפתור הסיכום האוטומטי
    st.markdown(f"""
    <div style="background-color: #f5f9ff; padding: 15px; border-radius: 10px; margin: 10px 0; direction: rtl; text-align: right;">
        <h4 style="color: #2c3e50; margin-bottom: 10px;">מצב בית הספר ביחס לממוצע הארצי:</h4>
        <ul style="list-style-type: none; padding-right: 10px;">
            <li>🧠 <strong>מיקוד שליטה פנימי (ICI):</strong> {ici_text}</li>
            <li>💪 <strong>חוסן (RISC):</strong> {risc_text}</li>
            <li>🕰️ <strong>תפיסות זמן:</strong>
                <ul style="list-style-type: none; padding-right: 20px;">
                    <li>• התמקדות בטראומות עבר: {future_negetive_past_text}</li>
                    <li>• התמקדות בזיכרונות חיוביים: {future_positive_past_text}</li>
                    <li>• תחושת חוסר שליטה בעתיד: {future_fatalic_present_text}</li>
                    <li>• חיים בהווה: {future_hedonistic_present_text}</li>
                    <li>• תכנון לטווח ארוך: {future_future_text}</li>
                </ul>
            </li>
        </ul>
    </div>    """, unsafe_allow_html=True)    # הוספת שאלות לחשיבה למנהל בהתבסס על נתוני בית הספר
    # יצירת פרומפט לשאילת שאלות בהתבסס על המדדים
    questions_prompt = f"""
    בהתבסס על הנתונים הבאים של בית הספר {selected_school}:

    1. מיקוד שליטה פנימי (ICI): {ici_text}
    2. חוסן (RISC): {risc_text}
    3. התמקדות בטראומות עבר: {future_negetive_past_text}
    4. התמקדות בזיכרונות חיוביים: {future_positive_past_text}
    5. תחושת חוסר שליטה בעתיד: {future_fatalic_present_text}
    6. חיים בהווה: {future_hedonistic_present_text}
    7. תכנון לטווח ארוך: {future_future_text}

    יצר בדיוק 2 שאלות עמוקות וממוקדות שיעזרו למנהל/ת בית הספר לחשוב על דרכים לשפר את המדדים האלה.
    השאלות צריכות להיות ממוקדות בתחומים הדורשים את השיפור הרב ביותר.
    """

    # מערכת פרומפט לשאלות חשיבה
    system_prompt = """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
    נדרשות ממך 2 שאלות מדויקות וממוקדות שיעזרו למנהל/ת בית הספר לחשוב כיצד לשפר את התחומים בהם נדרש שיפור.

    שאלות טובות הן כאלה ש:
    1. גורמות למנהל/ת לחשוב על מבנים קיימים בבית הספר
    2. מעוררות חשיבה על פעולות קונקרטיות שניתן לבצע
    3. מתמקדות בתחומים בהם נדרש שיפור משמעותי
    4. מחוברות לעולם המעשי של ניהול בית ספר

    הצג בדיוק 2 שאלות. כל שאלה צריכה להיות קצרה (2-3 שורות לכל היותר), ממוקדת וברורה.
    לא להוסיף שום טקסט מעבר לשאלות עצמן.
    אל תכתוב את מספרי השאלות.
    """

    try:
        # קריאה למודל השפה לקבלת 2 שאלות לחשיבה
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": questions_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # קבלת השאלות מהתשובה
        questions = response.choices[0].message.content.strip().split("\n")
          # סינון שורות ריקות
        questions = [q.strip() for q in questions if q.strip()]
        
        # הצגת השאלות בפורמט דומה לסיכום המדדים
        st.markdown(f"""
        <div style="background-color: #f5f9ff; padding: 15px; border-radius: 10px; margin: 10px 0; direction: rtl; text-align: right;">
            <h4 style="color: #2c3e50; margin-bottom: 10px;">🤔 שאלות לחשיבה:</h4>
            <ul style="list-style-type: none; padding-right: 10px;">
                <li><strong>שאלה 1:</strong> {questions[0] if len(questions) > 0 else ""}</li>
                <li><strong>שאלה 2:</strong> {questions[1] if len(questions) > 1 else ""}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"לא הצלחנו לייצר שאלות לחשיבה. שגיאה: {str(e)}")
   
    # כפתור ליצירת סיכום אוטומטי
    # if st.button("צור סיכום אוטומטי למנהל"):
    #     with st.spinner("מייצר סיכום..."):
    #         try:
    #             # קריאה לפונקציה ליצירת סיכום ב-LLM
    #             llm_summary = llms.generate_principal_summary(school_info_summary)
                
    #             # הצגת הסיכום בתיבה מעוצבת
    #             st.markdown("""
    #             <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px 0; direction: rtl; text-align: right;">
    #                 <h3 style="color: #2c3e50; margin-bottom: 15px;">סיכום אוטומטי - מבט מנהל</h3>
    #                 <div style="color: #34495e;">
    #                     {0}
    #                 </div>
    #             </div>
    #             """.format(llm_summary.replace("\n", "<br>")), unsafe_allow_html=True)
    #         except Exception as e:
    #             st.error(f"אירעה שגיאה בעת יצירת הסיכום: {str(e)}")


# הצגת סיכום מצב בית הספר בתחילת הדף
if selected_school and not filtered_df.empty:
    # יצירת אובייקט SchoolInfo לחישוב הנתונים
    school_info_summary = SchoolInfo(filtered_df)
    
    # חישוב הנתונים הרלוונטיים
    ici_text = school_info_summary.return_text_from_round_delta("ici")
    risc_text = school_info_summary.return_text_from_round_delta("risc")
    future_negetive_past_text = school_info_summary.return_text_from_round_delta("future_negetive_past")
    future_positive_past_text = school_info_summary.return_text_from_round_delta("future_positive_past")
    future_fatalic_present_text = school_info_summary.return_text_from_round_delta("future_fatalic_present")
    future_hedonistic_present_text = school_info_summary.return_text_from_round_delta("future_hedonistic_present")
    future_future_text = school_info_summary.return_text_from_round_delta("future_future")
      # בדיקה אם יש ערכים ממוצעים
    if hasattr(st.session_state, 'global_average'):
        # קבלת ערכי חוסן ומיקוד שליטה
        risc_value = school_info_summary.risc
        ici_value = school_info_summary.ici
        
        risc_avg = st.session_state.global_average["risc"]
        ici_avg = st.session_state.global_average["ici"]
          # קביעת מצב בית הספר ביחס לממוצע הארצי
        risc_status = "מעל הממוצע הארצי" if risc_value > risc_avg else "מתחת לממוצע הארצי"
        ici_status = "מעל הממוצע הארצי" if ici_value > ici_avg else "מתחת לממוצע הארצי"
        
        # קבלת המדד החלש ביותר
        worst_measure = school_info_summary.worst_anigma_name
        worst_statement = school_info_summary.worst_heg1_text
        
        # קבלת נתוני ממדי הזמן
        anigmas_dict = school_info_summary.return_anigmas_result_as_dict()
        
        # ניתוח תפיסות הזמן הבולטות ביותר (החיוביות והשליליות)
        time_perspectives = {
            "התמקדנות בטראומת עבר": {"value": anigmas_dict.get("future_negetive_past", 0), "avg": st.session_state.global_average.get("future_negetive_past", 0)},
            "התמקדנות בזיכרונות חיוביים": {"value": anigmas_dict.get("future_positive_past", 0), "avg": st.session_state.global_average.get("future_positive_past", 0)},
            "תחושה של חוסר שליטה על העתיד": {"value": anigmas_dict.get("future_fatalic_present", 0), "avg": st.session_state.global_average.get("future_fatalic_present", 0)},
            "חיים והתמקדות בהווה ובהנאות של כאן ועכשיו גם במחיר ויתור על העתידהווה" : {"value": anigmas_dict.get("future_hedonistic_present", 0), "avg": st.session_state.global_average.get("future_hedonistic_present", 0)},
            "תכנון לטווח הארוך והסתכלות קדימה": {"value": anigmas_dict.get("future_future", 0), "avg": st.session_state.global_average.get("future_future", 0)}
        }
        
        # מציאת תפיסת הזמן הגבוהה ביותר והנמוכה ביותר ביחס לממוצע
        strongest_perspective = max(time_perspectives.items(), key=lambda x: (x[1]["value"] - x[1]["avg"]) if x[1]["avg"] != 0 else 0)
        weakest_perspective = min(time_perspectives.items(), key=lambda x: (x[1]["value"] - x[1]["avg"]) if x[1]["avg"] != 0 else 0)
        
        # ניסוח הודעה על ממדי הזמן
        strongest_status = "גבוה במיוחד" if strongest_perspective[1]["value"] > strongest_perspective[1]["avg"] else "נמוך במיוחד"
        weakest_status = "נמוך במיוחד" if weakest_perspective[1]["value"] < weakest_perspective[1]["avg"] else "גבוה במיוחד"
        
        # # יצירת הסיכום בתיבה מודגשת
        # st.markdown("""
        # <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px 0; direction: rtl; text-align: right;">
        #     <h3 style="color: #1e3a8a; margin-bottom: 15px;">סיכום מצב בית הספר - למנהל</h3>
        #     <p><strong>חוסן</strong> של בית הספר נמצא <strong style="color: {0};">{1}</strong>.</p>
        #     <p><strong>מיקוד השליטה הפנימי</strong> של התלמידים נמצא <strong style="color: {2};">{3}</strong>.</p>
        #     <ul>
        #         <li><strong>{6}</strong> נמצא <strong style="color: {7};">{8}</strong> ביחס לממוצע הארצי.</li>
        #         <li> <strong>{9}</strong> נמצא <strong style="color: {10};">{11}</strong> ביחס לממוצע הארצי.</li>
        #     </ul>
        #     <p>תחום הדורש תשומת לב מיוחדת: <strong style="color: #d32f2f;">{4}</strong></p>
        #     <p style="font-style: italic; margin-top: 15px;">* המידע מבוסס על סקרים שהועברו לתלמידים. לחץ על הכפתורים מטה לניתוח מעמיק וקבלת המלצות מפורטות.</p>
        # </div>
        # """.format(
        #     "#2e7d32" if risc_status == "מעל הממוצע הארצי" else "#d32f2f",
        #     risc_status,
        #     "#2e7d32" if ici_status == "מעל הממוצע הארצי" else "#d32f2f",
        #     ici_status,
        #     worst_measure,
        #     worst_statement,
        #     strongest_perspective[0],  # שם הממד החזק ביותר
        #     "#2e7d32" if strongest_perspective[1]["value"] > strongest_perspective[1]["avg"] else "#d32f2f",  # צבע לממד החזק
        #     strongest_status,  # סטטוס הממד החזק
        #     weakest_perspective[0],  # שם הממד החלש ביותר
        #     "#d32f2f" if weakest_perspective[1]["value"] < weakest_perspective[1]["avg"] else "#2e7d32",  # צבע לממד החלש
        #     weakest_status  # סטטוס הממד החלש
        # ), unsafe_allow_html=True)


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
                
                ""
    # קבלת טקסט המתאר את מצב בית הספר בכל מדד ביחס לממוצע הארצי
            ici_text = school_info.return_text_from_round_delta("ici")
            risc_text = school_info.return_text_from_round_delta("risc")
            future_negetive_past_text = school_info.return_text_from_round_delta("future_negetive_past")
            future_positive_past_text = school_info.return_text_from_round_delta("future_positive_past")
            future_fatalic_present_text = school_info.return_text_from_round_delta("future_fatalic_present")
            future_hedonistic_present_text = school_info.return_text_from_round_delta("future_hedonistic_present")
            future_future_text = school_info.return_text_from_round_delta("future_future")
    #
    # # יצירת פרומפט למודל השפה
    # prompt = f"""
    
    # """
                  # יצירת פרומפט מסכם לכל הגרפים
            summary_prompt = f"""
                נתח את הנתונים הבאים של בית הספר {selected_school} ותן הסבר כולל על המשמעות שלהם:
                
                   אני מנהל/ת בית ספר ואני רוצה לקבל סיכום קצר וברור של מצב בית הספר שלי ביחס לממוצע הארצי,
                בהתבסס על הנתונים הבאים:
                הצג את הנתונים הבאים בצורה ברורה ומסודרת:
    
    1. מיקוד שליטה פנימי (ICI): {ici_text}
    2. חוסן (RISC): {risc_text}
    3. התמקדות בטראומות עבר (future_negetive_past): {future_negetive_past_text}
    4. התמקדות בזיכרונות חיוביים (future_positive_past): {future_positive_past_text}
    5. תחושת חוסר שליטה בעתיד (future_fatalic_present): {future_fatalic_present_text}
    6. חיים בהווה (future_hedonistic_present): {future_hedonistic_present_text}
    7. תכנון לטווח ארוך (future_future): {future_future_text}
    
               התייחס למשמעות המשולבת של כל המדדים והקשר ביניהם. תן ניתוח מעמיק של תפיסות הזמן והשפעתן על המדדים האחרים. תן שאלות מנחות למנהל בית הספר שיעזרו לו לשפר את המצב.
                """
                
                # מערכת פרומפט לניתוח מסכם           
            system_prompt = """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
                הסבר בבקשה את המשמעות המשולבת של כל המדדים הבאים עבור בית הספר והקשר ביניהם.
                
                מדד החוסן (RISC) - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
                
                מיקוד שליטה פנימי (ICI) - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית חזקה יותר.
                
                תפיסות זמן - חמישה ממדים:
                1. התמקדות בחוויות טראומתיות מהעבר- תפיסה שלילית של העבר, טראומות וחוויות קשות. ערך גבוה מעיד על נטייה להתמקד בחוויות שליליות מהעבר.
                2.  התמקדות בזכרונות חיוביים מהעבר- תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים. ערך גבוה מעיד על תחושת ביטחון ושורשיות.
                3. תחושה של חוסר שליטה על העתיד- תפיסה פטליסטית של ההווה, אמונה שהכל נקבע מראש וחוסר שליטה. ערך גבוה מעיד על תחושת חוסר אונים.
                4. חיים והתמקדות בהווה ובהנאות של כאן ועכשיו גם במחיר ויתור על העתיד - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות וחוסר תכנון. ערך גבוה מעיד על התמקדות בסיפוקים מיידיים.
                5. תכנון לטווח הארוך והסתכלות קדימה - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות. ערך גבוה מעיד על אוריינטציה לעתיד ויכולת תכנון.
                
                
                בניתוח שלך, התייחס למשמעות של אחוזים גבוהים ונמוכים בכל מדד ולהשפעה ההדדית ביניהם. התייחס גם לאיזון בין המדדים השונים.
                
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
        
תן 2 שאלות למנהל שיעזרו לו לחשוב ולהתבונן על הבית ספר שלו לפי ההיגד הבעייתי ולפי המדד החלש ביותר . שאלות אלו יעזרו לו לחשוב ולראות כיצד הוא יכול להשתפר. 
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

if st.button("הצג לי גרפים") or st.session_state.show_graphs_state:
        # עדכון המצב לזכור שהגרפים הוצגו
        st.session_state.show_graphs_state = True
        
            # הוספת הסבר קצר לגרף חוסן
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 30px; direction: rtl; text-align: right;">
            <h4 style="color: #2c3e50; margin-bottom: 10px;">איך לקרוא את הגרפים?</h4>
            <p>הגרפים מציגים את הנתונים של בית הספר שלך בהשוואה לממוצעים חשובים:</p>
            <ul style="list-style-type: none; padding-right: 0; margin-top: 10px;">
            <li style="margin-bottom: 5px;">🟢 <strong>קו ירוק</strong> - הממוצע בבית הספר שלך</li>
            <li style="margin-bottom: 5px;">🔵 <strong>קו כחול</strong> - הממוצע הארצי של בתי הספר שהשתתפו במחקר</li>
            <li style="margin-bottom: 5px;">🟠 <strong>קו כתום</strong> - הממוצע במחקר הבינלאומי (בעיקר מארה"ב)</li>
            </ul>
            <p style="margin-top: 10px;">לניתוח מעמיק של הנתונים, לחצו על כפתור "הראה לי ניתוח מקיף".</p>
        </div>
        """, unsafe_allow_html=True)
        
        # הצגת גרף חוסן        st.markdown("### מדד חוסן")
        fig_risc = school_info.get_fig_risc("חוסן")
        st.plotly_chart(fig_risc, use_container_width=True, key="risc_chart_1")

    

        # שמירת נתוני גרף חוסן למצב
        st.session_state.graph_data["risc"] = {
            "value": school_info.risc,
            "global_avg": st.session_state.global_average["risc"],
            "research_avg": st.session_state.research_average["risc"]
        }        # הצגת גרף מיקוד שליטה
        st.markdown("### מיקוד שליטה פנימי")
        fig_ici = school_info.get_fig_ici("מיקוד שליטה")
        st.plotly_chart(fig_ici, use_container_width=True, key="ici_chart_1")

       # שמירת נתוני גרף מיקוד שליטה למצב
        st.session_state.graph_data["ici"] = {
            "value": school_info.ici,
            "global_avg": st.session_state.global_average["ici"],
            "research_avg": st.session_state.research_average["ici"]
        }        # הצגת גרף עכביש
        st.markdown("### התפלגות לפי ממדי זמן")
             # הוספת הסבר קצר לגרף עכביש
        st.markdown("""
        <div style="direction: rtl; text-align: right; margin-bottom: 30px;">
            <p>גרף זה מציג את פרופיל תפיסת הזמן של בית הספר שלך, כאשר כל ציר מייצג ממד זמן אחר.</p>
            <ul style="list-style-type: none; padding-right: 0;">
            <li>🟢 <strong>הקו הירוק</strong> - הממוצע בבית הספר שלך</li>
            <li>🔵 <strong>הקו הכחול</strong> - הממוצע הארצי של בתי הספר שהשתתפו במחקר</li>
            <li>🟠 <strong>הקו הכתום</strong> - הממוצע במחקר הבינלאומי (בעיקר מארה"ב)</li>
            </ul>
            <p>למידע מעמיק יותר, לחצו על כפתור "הראה לי ניתוח מקיף".</p>
        </div>
        """, unsafe_allow_html=True)
        fig_spider = school_info.get_fig_spider()
        st.plotly_chart(fig_spider, use_container_width=True, key="spider_chart_1")

   

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
# # כפתור להצגת סיכום טקסטואלי בהתבסס על return_text_from_round_delta
# if st.button("הצג סיכום טקסטואלי על המדדים", key="text_summary_button"):
#     if selected_school and not filtered_df.empty:
#         summary_placeholder = st.empty()
#         summary_placeholder.markdown("מכין סיכום טקסטואלי...")
        
#         try:
#             # יצירת אובייקט SchoolInfo חדש
#             updated_school_info = SchoolInfo(filtered_df)
            
#             # קבלת הטקסט מהמתודה return_text_from_round_delta עבור כל מדד
#             ici_text = updated_school_info.return_text_from_round_delta("ici")
#             risc_text = updated_school_info.return_text_from_round_delta("risc")
#             future_negetive_past_text = updated_school_info.return_text_from_round_delta("future_negetive_past")
#             future_positive_past_text = updated_school_info.return_text_from_round_delta("future_positive_past")
#             future_fatalic_present_text = updated_school_info.return_text_from_round_delta("future_fatalic_present")
#             future_hedonistic_present_text = updated_school_info.return_text_from_round_delta("future_hedonistic_present")
#             future_future_text = updated_school_info.return_text_from_round_delta("future_future")
            
#             # יצירת סיכום HTML
#             summary_html = f"""
#             <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-top: 20px; margin-bottom: 20px; direction: rtl; text-align: right;">
#                 <h2 style="color: #1565c0; text-align: center; margin-bottom: 20px;">סיכום מצב בית הספר {selected_school} ביחס לממוצע הארצי</h2>
                
#                 <div style="margin-bottom: 15px;">
#                     <h3 style="color: #333; margin-bottom: 5px;">מדדים מרכזיים:</h3>
#                     <ul style="list-style-type: none; padding-right: 10px;">
#                         <li style="margin-bottom: 8px;"><strong>מיקוד שליטה פנימי (ICI):</strong> <span style="color: {get_color_for_text(ici_text)};">{ici_text}</span></li>
#                         <li style="margin-bottom: 8px;"><strong>חוסן (RISC):</strong> <span style="color: {get_color_for_text(risc_text)};">{risc_text}</span></li>
#                     </ul>
#                 </div>
                
#                 <div style="margin-bottom: 15px;">
#                     <h3 style="color: #333; margin-bottom: 5px;">תפיסות זמן:</h3>
#                     <ul style="list-style-type: none; padding-right: 10px;">
#                         <li style="margin-bottom: 8px;"><strong>התמקדות בחוויות טראומתיות מהעבר:</strong> <span style="color: {get_color_for_text(future_negetive_past_text)};">{future_negetive_past_text}</span></li>
#                         <li style="margin-bottom: 8px;"><strong>התמקדות בזכרונות חיוביים מהעבר:</strong> <span style="color: {get_color_for_text(future_positive_past_text)};">{future_positive_past_text}</span></li>
#                         <li style="margin-bottom: 8px;"><strong>תחושה של חוסר שליטה על העתיד:</strong> <span style="color: {get_color_for_text(future_fatalic_present_text)};">{future_fatalic_present_text}</span></li>
#                         <li style="margin-bottom: 8px;"><strong>חיים והתמקדות בהווה ובהנאות של כאן ועכשיו:</strong> <span style="color: {get_color_for_text(future_hedonistic_present_text)};">{future_hedonistic_present_text}</span></li>
#                         <li style="margin-bottom: 8px;"><strong>תכנון לטווח הארוך והסתכלות קדימה:</strong> <span style="color: {get_color_for_text(future_future_text)};">{future_future_text}</span></li>
#                     </ul>
#                 </div>
                
#                 <div style="margin-top: 20px; font-style: italic; color: #555; text-align: center;">
#                     הנתונים מבוססים על השוואה לממוצע הארצי של כלל בתי הספר שהשתתפו במחקר.
#                 </div>
#             </div>
#             """
            
#             # הצגת הסיכום
#             summary_placeholder.markdown(summary_html, unsafe_allow_html=True)
            
#         except Exception as e:
#             error_msg = f"לא הצלחנו לייצר סיכום טקסטואלי. שגיאה: {str(e)}"
#             summary_placeholder.error(error_msg)
#     else:
#         st.error("לא נבחר בית ספר או שאין נתונים זמינים.")

# # פונקציה להגדרת צבע על פי סוג הטקסט
# def get_color_for_text(text):
#     if "מעל" in text or "גבוה" in text:
#         return "#2e7d32"  # ירוק
#     elif "מתחת" in text or "נמוך" in text:
#         return "#d32f2f"  # אדום
#     else:
#         return "#757575"  # אפור


