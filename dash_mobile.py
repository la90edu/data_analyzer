import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

# Import custom modules
import llm_system_massage_manager
import llm_gpt
import draw_gauge
import draw_spider_graph
import draw_bar_chart
import connect_to_google_sheet
import consts
import anigmas
from class_school_info import SchoolInfo
from graph_manager import Gauge_Graph_type, Spider_Graph_type, Bar_Chart_Graph_type
from system_prompt import return_prompt,return_highlighted_text
# טעינת משתני הסביבה מקובץ .env
load_dotenv()

# קבלת ה-API key מהמשתנים והגדרת הלקוח
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai_client = OpenAI(api_key=api_key)
else:
    openai_client = OpenAI()  # יתכן שיעבוד אם יש API key בסביבה

# Page Configuration
st.set_page_config(
    page_title="דאשבורד ניתוח נתונים",
    page_icon="📊",
    layout="wide",
)

# Add RTL support and custom styling
st.markdown(
    """
    <style>
    /* RTL Support */
    h1, h2, h3, h4, h5, h6, p, div {
        text-align: right;
        direction: rtl;
    }
    
    /* Sidebar open by default */
    [data-testid="stSidebar"][aria-expanded="true"] {
        width: 300px !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 300px !important;
        margin-left: -300px;
    }
    
    /* Force sidebar to be open on page load */
    section[data-testid="stSidebar"] {
        display: block !important;
        opacity: 1 !important;
        transform: none !important;
    }
    
    /* Dashboard Layout Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Card styling for graphs */
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    /* שיפור גודל העמודות למניעת דחיסה של הגרפים */
    .row-widget.stButton, [data-testid="stVerticalBlock"] > div {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* וידוא שהגרפים מקבלים את הרוחב המתאים */
    [data-testid="column"] {
        width: auto !important;
        min-width: 0;
        flex: 1;
    }
    
    /* עיצוב רכיב בחירת בית ספר בחלק העליון */
    .school-selector {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .school-selector .stSelectbox {
        max-width: 400px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize data
def init():
    data = connect_to_google_sheet.return_data()
    df = pd.DataFrame(data)
    consts.init_st_session_global_average_and_research_average(df)
    consts.init_heg_avg(df)
    return df

#knowledge_files=

# Initialize session state for chat and graph data
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "graph_data" not in st.session_state:
    st.session_state.graph_data = {
        "risc": None,
        "ici": None, 
        "spider": None,
        "selected_school": None
    }

# Initialize session state for graph explanations
if "graph_explanations" not in st.session_state:
    st.session_state.graph_explanations = {
        "risc": {"show": False, "explanation": ""},
        "ici": {"show": False, "explanation": ""},
        "spider": {"show": False, "explanation": ""}
    }

# הפונקציה המשופרת לקבלת תשובה מ-OpenAI עם תמיכה בנתוני הגרפים ובסטרימינג
def get_openai_response(prompt, system_prompt, history, graph_data, stream=False):
    # יצירת תקציר של נתוני הגרפים כדי להעביר אותם לצ'אטבוט
    graph_summary = ""
    if graph_data["selected_school"]:
        graph_summary += f"הנתונים שלהלן מתייחסים לבית הספר: {graph_data['selected_school']}\n\n"
    
    if graph_data["risc"] is not None:
        graph_summary += f"נתוני גרף חוסן :\n"
        graph_summary += f"ערך נוכחי: {graph_data['risc']['value']:.2f}\n"
        graph_summary += f"ממוצע ארצי: {graph_data['risc']['global_avg']:.2f}\n"
        #graph_summary += f"ממוצע מחקרי: {graph_data['risc']['research_avg']:.2f}\n\n"
        
    if graph_data["ici"] is not None:
        graph_summary += f"נתוני גרף מיקוד שליטה פנימי (ICI):\n"
        graph_summary += f"ערך נוכחי: {graph_data['ici']['value']:.2f}\n"
        graph_summary += f"ממוצע ארצי: {graph_data['ici']['global_avg']:.2f}\n"
       # graph_summary += f"ממוצע מחקרי: {graph_data['ici']['research_avg']:.2f}\n\n"
        
    if graph_data["spider"] is not None:
        graph_summary += f"לתפיסות זמן:\n"
        
        for category, values in graph_data["spider"].items():
            formatted_category = category.replace("future_", "").replace("_past", "").replace("_present", "")
            graph_summary += f"קטגוריה: {formatted_category}\n"
            graph_summary += f"  ערך נוכחי: {values['current']:.2f}\n"
            graph_summary += f"  ממוצע ארצי: {values['global']:.2f}\n"
            #graph_summary += f"  ממוצע מחקרי: {values['research']:.2f}\n"
    
    # הוספת הנחיות ספציפיות לגרפים בפרומפט המערכת
    graph_system_prompt = system_prompt + ""

    
    # הוספת תקציר הגרפים לפרומפט המשתמש
    user_prompt = f"""history: {history}

current prompt: {prompt}

נתוני הגרפים המוצגים בדאשבורד:
{graph_summary}
"""
    
    try:
        if stream:
            # החזר אובייקט סטרימינג שניתן לאיטרציה
            response_stream = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": graph_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.05,  # הוספת טמפרטורה נמוכה לתשובות יותר ממוקדות
                stream=True
            )
            return response_stream
        else:
            # החזרת תשובה מלאה (ללא סטרימינג)
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": graph_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.05  # הוספת טמפרטורה נמוכה לתשובות יותר ממוקדות
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"אירעה שגיאה בעת התקשורת עם OpenAI: {str(e)}"

# Streamed response generator for chatbot
def response_generator(prompt, df, graph_data,school_info):
    data = df.to_markdown()
    system_prompt = return_prompt(school_info) #llm_system_massage_manager.get_first_system_prompt(data)
    
    # קבלת התשובה באמצעות ה-API Key מקובץ .env והעברת נתוני הגרפים
    # עם סטרימינג מופעל
    response_stream = get_openai_response(prompt, system_prompt, st.session_state.messages, graph_data, stream=True)
    
    full_response = ""
    # לולאה על אירועי הסטרים מ-OpenAI
    for chunk in response_stream:
        if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content  # שליחת כל חלק שמתקבל מידית לתצוגה
    
    # החזרת התשובה המלאה לצורך שמירה בהיסטוריה
    return full_response

# פונקציה לקבלת הסבר על גרף ספציפי
def get_graph_explanation(graph_type, graph_data, school_info=None):
    """
    מקבלת הסבר על גרף ספציפי ממודל השפה
    
    Args:
        graph_type: סוג הגרף (risc, ici, spider)
        graph_data: הנתונים של הגרף
        school_info: אובייקט SchoolInfo אם קיים
    
    Returns:
        הסבר טקסטואלי מפורט על הגרף ומשמעותו
    """
    if graph_type == "risc":
        prompt = f"""
        הסבר בבקשה את נתוני גרף החוסן הבאים:
        ערך נוכחי: {graph_data['value']:.2f}
        ממוצע ארצי: {graph_data['global_avg']:.2f}
        
        מה המשמעות של הנתונים האלה? האם הערך גבוה או נמוך ביחס לממוצע? מה זה אומר על בית הספר?
        התייחס להשלכות החינוכיות והחברתיות של התוצאות. תן המלצות להמשך בהתבסס על הנתונים.
        """
    elif graph_type == "ici":
        prompt = f"""
        הסבר בבקשה את נתוני גרף מיקוד שליטה פנימי (ICI) הבאים:
        ערך נוכחי: {graph_data['value']:.2f}
        ממוצע ארצי: {graph_data['global_avg']:.2f}
        
        מה המשמעות של הנתונים האלה? האם הערך גבוה או נמוך ביחס לממוצע? מה זה אומר על בית הספר?
        התייחס להשלכות החינוכיות והחברתיות של התוצאות. תן המלצות להמשך בהתבסס על הנתונים.
        """
    elif graph_type == "spider":
        prompt = """
        הסבר בבקשה את נתוני גרף תפיסות הזמן (גרף העכביש) המוצג.
        מהי המשמעות של כל אחד מהממדים? אילו ממדים בולטים לטובה ואילו לרעה?
        מהן ההשלכות החינוכיות והפסיכולוגיות של התוצאות?
        תן המלצות להמשך בהתבסס על הנתונים.
        """
        
        # הוספת פירוט על הקטגוריות בגרף העכביש אם יש נתונים
        if graph_data:
            prompt += "\n\nנתוני הקטגוריות השונות:\n"
            for category, values in graph_data.items():
                formatted_category = category.replace("future_", "").replace("_past", "").replace("_present", "")
                if "current" in values and "global" in values:
                    prompt += f"- {formatted_category}: ערך נוכחי {values['current']:.2f}, ממוצע ארצי {values['global']:.2f}\n"
    
    # הוספת מידע על בית הספר אם קיים
    if school_info and hasattr(school_info, 'school_name'):
        prompt += f"\nהנתונים מתייחסים לבית הספר: {school_info.school_name}"
    
    try:
        system_prompt = """אתה יועץ חינוכי מומחה בניתוח נתונים פסיכולוגיים של תלמידים. 
        עליך להסביר את משמעות הנתונים בצורה ברורה, מקצועית ומעשית.
        
        מדד החוסן (RISC) - מודד את יכולת התלמידים להתמודד עם אתגרים ומצבי לחץ. ערכים גבוהים מעידים על חוסן גבוה.
        
        מיקוד שליטה פנימי (ICI) - מודד את האמונה של התלמידים ביכולתם לשלוט בחייהם. ערכים גבוהים מעידים על תחושת שליטה עצמית.
        
        תפיסות זמן (גרף עכביש) - מציג חמישה ממדים:
        1. עבר שלילי - תפיסה שלילית של העבר, טראומות וחוויות קשות
        2. עבר חיובי - תפיסה חיובית של העבר, נוסטלגיה וזכרונות טובים
        3. הווה דטרמיניסטי - תפיסה פטליסטית של ההווה, חוסר שליטה
        4. הווה הדוניסטי - תפיסת הווה הדוניסטית, חיפוש הנאות מיידיות
        5. עתיד - יכולת תכנון קדימה, דחיית סיפוקים, הצבת מטרות
        
        התייחס בהסבר שלך להשלכות החינוכיות והמעשיות של הנתונים.
        """
        
        # השתמש ב-OpenAI API לקבלת הסבר
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # או מודל אחר שתרצה להשתמש בו
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        explanation = response.choices[0].message.content
        
        # אם התשובה ריקה או קצרה מדי, החזר הסבר כללי יותר
        if not explanation or len(explanation) < 20:
            if graph_type == "risc":
                return "חוסן מתייחס ליכולת של תלמידים להתמודד עם אתגרים ומצבי לחץ. ככל שהציון גבוה יותר, כך התלמידים מראים יכולת טובה יותר להתמודדות עם קשיים."
            elif graph_type == "ici":
                return "מיקוד שליטה פנימי (ICI) מתייחס למידה שבה אדם מאמין שהוא שולט בחייו. ציון גבוה מעיד על תחושת שליטה עצמית גבוהה, בעוד ציון נמוך מעיד על תפיסה שגורמים חיצוניים שולטים בחייו."
            elif graph_type == "spider":
                return "גרף העכביש מציג חמישה ממדים של תפיסת זמן: עבר שלילי, עבר חיובי, הווה דטרמיניסטי, הווה הדוניסטי, ועתיד. האיזון בין ממדים אלו משפיע על קבלת החלטות ותפיסת העולם של התלמידים."
        
        return explanation
    
    except Exception as e:
        # במקרה של שגיאה, החזר הסבר כללי והודעת שגיאה
        error_msg = f"לא הצלחנו לייצר הסבר אוטומטי. שגיאה: {str(e)}"
        st.error(error_msg)
        
        # הסבר ברירת מחדל לפי סוג הגרף
        if graph_type == "risc":
            return "חוסן (RISC): מודד את היכולת של התלמידים להתמודד עם אתגרים ומצבי לחץ. ציון גבוה מעיד על יכולת התמודדות טובה יותר."
        elif graph_type == "ici":
            return "מיקוד שליטה פנימי (ICI): מודד את האמונה של אדם שהוא שולט בחייו ולא גורמים חיצוניים. ציון גבוה מעיד על תחושת מסוגלות עצמית חזקה יותר."
        elif graph_type == "spider":
            return "גרף תפיסות זמן: מציג את החלוקה של תפיסות הזמן השונות (עבר שלילי/חיובי, הווה דטרמיניסטי/הדוניסטי, עתיד). איזון נכון בין התפיסות חשוב להתנהגות בריאה והצלחה לימודית."
        else:
            return "לא הצלחנו לייצר הסבר אוטומטי לגרף זה."

# Main Dashboard
def main():
    st.title("דאשבורד ניתוח נתונים 📊")
    st.markdown("### ניתוח נתונים חינוכיים עם גרפים ואינטראקציה")
    
    # הוספת גילוי מובייל משופר עם JavaScript
    st.markdown(
        """
        <script>
            // העברת רוחב החלון לאפליקציה
            window.addEventListener('DOMContentLoaded', function() {
                const width = window.innerWidth;
                // הוספת סימון לתצוגת מובייל
                if (width < 768) {
                    document.documentElement.classList.add('mobile-view');
                    document.body.style.setProperty('--screen-width', width + 'px');
                }
            });
            // התאמת הסיידבר למובייל
            window.addEventListener('resize', function() {
                const width = window.innerWidth;
                if (width < 768) {
                    document.documentElement.classList.add('mobile-view');
                } else {
                    document.documentElement.classList.remove('mobile-view');
                }
                document.body.style.setProperty('--screen-width', width + 'px');
            });
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # הוספת CSS ספציפי למובייל למקרה שבו יש צורך בהתאמות נוספות
    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            /* עיצוב משופר לסיידבר במובייל */
            [data-testid="stSidebar"] {
                border-radius: 0 !important;
            }
            
            /* מרווחים טובים יותר עבור בחירת בית ספר במובייל */
            div[data-testid="stSelectbox"] {
                margin-bottom: 1rem !important;
                width: 100% !important;
            }
            
            /* שיפור מראה אזהרות במובייל */
            [data-testid="stAlert"] {
                padding: 8px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Load data
    try:
        df = init()
    except Exception as e:
        st.error(f"Aאירעה שגיאה בטעינת הנתונים: {e}")
        df = pd.DataFrame()  # Empty dataframe as fallback
    
    # בחירת בית ספר בחלק העליון של העמוד
    selected_school = None
    if not df.empty and 'school' in df.columns:
        # מיכל עם עיצוב מותאם לבחירת בית הספר
        school_selector_container = st.container()
        with school_selector_container:
            st.markdown('<div class="school-selector">', unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; margin-bottom: 15px;'>בחירת בית ספר</h3>", unsafe_allow_html=True)
            unique_schools = df["school"].unique().tolist()
            selected_school = st.selectbox("בחר בית ספר:", unique_schools, key="school_selector_top")
            st.markdown('</div>', unsafe_allow_html=True)
            
        filtered_df = df[df['school'] == selected_school]
        st.session_state.graph_data["selected_school"] = selected_school
    else:
        # Demo data if no real data is available
        filtered_df = df
        st.warning("לא נמצאו נתונים לסינון")
    
    # הוספת CSS ספציפי למובייל אם נדרש
    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            /* הסתרת הסיידבר במובייל */
            [data-testid="stSidebar"] {
                display: none;
            }
            
            /* התאמת תוכן הדף למלוא רוחב המסך */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # בדיקה מובייל - אם רוחב המסך קטן מ-768px, נציג את הגרפים אחד מתחת לשני
    # Initialize mobile detection in session state if not already set
    if "is_mobile" not in st.session_state:
        st.session_state.is_mobile = False
        
    # # Option 1: Allow manual toggle for mobile view in sidebar
    # with st.sidebar:
    #     st.session_state.is_mobile = st.checkbox("תצוגת מובייל", value=st.session_state.is_mobile)
    
    is_mobile = True #st.session_state.is_mobile
    
    if is_mobile:
        # במובייל - כל גרף בקולונה נפרדת אחד מתחת לשני
        st.markdown("<p style='font-size:0.8rem;color:#666;'>תצוגת מובייל מופעלת</p>", unsafe_allow_html=True)
        row1_col1 = st.container()
        row1_col2 = st.container()
        row1_col3 = st.container()
    else:
        # בדסקטופ - שלושה גרפים בשורה
        row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    # Generate sample graphs if no data
    if filtered_df.empty:
        # Sample data for demonstration
        with row1_col1:
            st.markdown("### מדד חוסן")
            fig1 = generate_sample_gauge()
            st.plotly_chart(fig1, use_container_width=True)
            
            # שמירת נתוני גרף לדוגמה לצ'אטבוט
            st.session_state.graph_data["risc"] = {
                "value": 3.7,
                "global_avg": 3.5,
                "research_avg": 3.8
            }
            
            # כפתור "מה זה אומר?" עבור גרף החוסן
            if st.button("מה זה אומר?", key="explain_risc"):
                if not st.session_state.graph_explanations["risc"]["explanation"]:
                    explanation = get_graph_explanation("risc", st.session_state.graph_data["risc"])
                    st.session_state.graph_explanations["risc"]["explanation"] = explanation
                
                st.session_state.graph_explanations["risc"]["show"] = not st.session_state.graph_explanations["risc"]["show"]
            
            # הצגת ההסבר אם הכפתור נלחץ
            if st.session_state.graph_explanations["risc"]["show"]:
                st.markdown(f"""<div class="explanation-box">
                {st.session_state.graph_explanations["risc"]["explanation"]}
                </div>""", unsafe_allow_html=True)
            
        with row1_col2:
            st.markdown("### מיקוד שליטה פנימי")
            fig2 = generate_sample_gauge(value=3.4, title="מיקוד שליטה פנימי")
            st.plotly_chart(fig2, use_container_width=True)
            
            # שמירת נתוני גרף לדוגמה לצ'אטבוט
            st.session_state.graph_data["ici"] = {
                "value": 3.4,
                "global_avg": 3.2,
                "research_avg": 3.6
            }
            
            # כפתור "מה זה אומר?" עבור גרף מיקוד שליטה פנימי
            if st.button("מה זה אומר?", key="explain_ici"):
                if not st.session_state.graph_explanations["ici"]["explanation"]:
                    explanation = get_graph_explanation("ici", st.session_state.graph_data["ici"])
                    st.session_state.graph_explanations["ici"]["explanation"] = explanation
                
                st.session_state.graph_explanations["ici"]["show"] = not st.session_state.graph_explanations["ici"]["show"]
            
            # הצגת ההסבר אם הכפתור נלחץ
            if st.session_state.graph_explanations["ici"]["show"]:
                st.markdown(f"""<div class="explanation-box">
                {st.session_state.graph_explanations["ici"]["explanation"]}
                </div>""", unsafe_allow_html=True)
            
        with row1_col3:
            st.markdown("### נתוני ציר הזמן")
            fig3 = generate_sample_spider()
            st.plotly_chart(fig3, use_container_width=True)
            
            # שמירת נתוני גרף לדוגמה לצ'אטבוט
            st.session_state.graph_data["spider"] = {
                "negetive_past": {"current": 3.2, "global": 3.0, "research": 2.8},
                "positive_past": {"current": 4.1, "global": 3.8, "research": 4.0},
                "fatalic_present": {"current": 2.8, "global": 3.0, "research": 2.5},
                "hedonistic_present": {"current": 3.5, "global": 3.2, "research": 3.0},
                "future": {"current": 3.9, "global": 3.7, "research": 4.0},
            }
            
            # כפתור "מה זה אומר?" עבור גרף תפיסות זמן
            if st.button("מה זה אומר?", key="explain_spider"):
                if not st.session_state.graph_explanations["spider"]["explanation"]:
                    explanation = get_graph_explanation("spider", st.session_state.graph_data["spider"])
                    st.session_state.graph_explanations["spider"]["explanation"] = explanation
                
                st.session_state.graph_explanations["spider"]["show"] = not st.session_state.graph_explanations["spider"]["show"]
            
            # הצגת ההסבר אם הכפתור נלחץ
            if st.session_state.graph_explanations["spider"]["show"]:
                st.markdown(f"""<div class="explanation-box">
                {st.session_state.graph_explanations["spider"]["explanation"]}
                </div>""", unsafe_allow_html=True)
    else:
        # Real graphs from data
        try:
            school_info = SchoolInfo(filtered_df)
            
            with row1_col1:
                st.markdown("### מדד חוסן")
                fig_risc = school_info.get_fig_risc("חוסן")
                st.plotly_chart(fig_risc, use_container_width=True)
                
                # שמירת נתוני גרף אמיתיים לצ'אטבוט
                st.session_state.graph_data["risc"] = {
                    "value": school_info.risc,
                    "global_avg": st.session_state.global_average["risc"],
                    "research_avg": st.session_state.research_average["risc"]
                }
                
                # כפתור "מה זה אומר?" עבור גרף החוסן האמיתי
                if st.button("מה זה אומר?", key="explain_risc_real"):
                    if not st.session_state.graph_explanations["risc"]["explanation"]:
                        explanation = get_graph_explanation("risc", st.session_state.graph_data["risc"], school_info)
                        st.session_state.graph_explanations["risc"]["explanation"] = explanation
                    
                    st.session_state.graph_explanations["risc"]["show"] = not st.session_state.graph_explanations["risc"]["show"]
                
                # הצגת ההסבר אם הכפתור נלחץ
                if st.session_state.graph_explanations["risc"]["show"]:
                    st.markdown(f"""<div class="explanation-box">
                    {st.session_state.graph_explanations["risc"]["explanation"]}
                    </div>""", unsafe_allow_html=True)
                
            with row1_col2:
                st.markdown("### מיקוד שליטה פנימי")
                fig_ici = school_info.get_fig_ici("מיקוד שליטה")
                st.plotly_chart(fig_ici, use_container_width=True)
                
                # שמירת נתוני גרף אמיתיים לצ'אטבוט
                st.session_state.graph_data["ici"] = {
                    "value": school_info.ici,
                    "global_avg": st.session_state.global_average["ici"],
                    "research_avg": st.session_state.research_average["ici"]
                }
                
                # כפתור "מה זה אומר?" עבור גרף מיקוד שליטה אמיתי
                if st.button("מה זה אומר?", key="explain_ici_real"):
                    if not st.session_state.graph_explanations["ici"]["explanation"]:
                        explanation = get_graph_explanation("ici", st.session_state.graph_data["ici"], school_info)
                        st.session_state.graph_explanations["ici"]["explanation"] = explanation
                    
                    st.session_state.graph_explanations["ici"]["show"] = not st.session_state.graph_explanations["ici"]["show"]
                
                # הצגת ההסבר אם הכפתור נלחץ
                if st.session_state.graph_explanations["ici"]["show"]:
                    st.markdown(f"""<div class="explanation-box">
                    {st.session_state.graph_explanations["ici"]["explanation"]}
                    </div>""", unsafe_allow_html=True)
                
            with row1_col3:
                st.markdown("### התפלגות לפי ממדי זמן")
                fig_spider = school_info.get_fig_spider()
                st.plotly_chart(fig_spider, use_container_width=True)
                
                # שמירת נתוני גרף אמיתיים לצ'אטבוט
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
                
                # כפתור "מה זה אומר?" עבור גרף תפיסות זמן אמיתי
                if st.button("מה זה אומר?", key="explain_spider_real"):
                    if not st.session_state.graph_explanations["spider"]["explanation"]:
                        explanation = get_graph_explanation("spider", st.session_state.graph_data["spider"], school_info)
                        st.session_state.graph_explanations["spider"]["explanation"] = explanation
                    
                    st.session_state.graph_explanations["spider"]["show"] = not st.session_state.graph_explanations["spider"]["show"]
                
                # הצגת ההסבר אם הכפתור נלחץ
                if st.session_state.graph_explanations["spider"]["show"]:
                    st.markdown(f"""<div class="explanation-box">
                    {st.session_state.graph_explanations["spider"]["explanation"]}
                    </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"שגיאה בעת יצירת הגרפים: {e}")
    
    # Divider - הועבר למקום הזה שהוא מתחת לכל הגרפים והכפתורים
    st.markdown("---")
    
    # Chatbot section with API key information
    st.markdown("### צ'אטבוט לניתוח נתונים 🤖")
    
    short=llm_gpt.return_llm_answer(return_highlighted_text(school_info),"","")
    # Show API status
    if api_key:
        st.success(short)
    else:
        st.warning("לא נמצא API key של OpenAI. הצ'אטבוט עשוי לא לפעול כראוי.")
    
    st.markdown("שאל שאלות על הנתונים המוצגים בגרפים או על התוצאות הכלליות")
    
    # הצעות לשאלות למשתמש
    suggested_questions = [
        "הכן דוח מנהל",
    ]
    
    # ממשק משתמש שמראה הצעות לשאלות
    st.markdown("#### שאלות לדוגמה:")
    cols = st.columns(3)
    for i, question in enumerate(suggested_questions):
        col_idx = i % 3
        if cols[col_idx].button(question, key=f"question_{i}"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": question})
            
            # מציגים את שאלת המשתמש
            with st.chat_message("user"):
                st.markdown(question)
                
            # מציגים את תשובת הצ'אטבוט עם סטרימינג בזמן אמת
            with st.chat_message("assistant"):
                data = filtered_df.to_markdown() if not filtered_df.empty else "אין נתונים זמינים"
                system_prompt = return_prompt(school_info) #llm_system_massage_manager.get_first_system_prompt(data)
                
                # שימוש בסטרימינג עבור שאלות דוגמה
                response_stream = get_openai_response(
                    question, 
                    system_prompt, 
                    st.session_state.messages[:-1], 
                    st.session_state.graph_data,
                    stream=True
                )
                
                # מקום להצגת התשובה המתעדכנת
                message_placeholder = st.empty()
                full_response = ""
                
                # לולאה על אירועי הסטרים מ-OpenAI והצגתם בזמן אמת
                for chunk in response_stream:
                    if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            # מציג את התשובה המתעדכנת עם סמן מהבהב
                            message_placeholder.markdown(full_response + "▌")
                
                # הצגת התשובה המלאה הסופית (ללא הסמן)
                message_placeholder.markdown(full_response)
            
            # הוספת התשובה להיסטוריה
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # הצגת היסטוריית צ'אט (רק מהיסטוריה קודמת)
    messages_to_display = st.session_state.messages[:-2] if len(st.session_state.messages) >= 2 else []
    if messages_to_display:
        st.markdown("#### היסטוריית צ'אט:")
        chat_container = st.container()
        with chat_container:
            for message in messages_to_display:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
    # Input for chat
    if prompt := st.chat_input("שאל שאלה על הנתונים..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # מציגים את שאלת המשתמש
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # מציגים את תשובת הצ'אטבוט עם סטרימינג בזמן אמת
        with st.chat_message("assistant"):
            # מקום להצגת התשובה המתעדכנת
            message_placeholder = st.empty()
            full_response = ""
            
            # קבלת תשובה מהצ'אטבוט עם סטרימינג
            response_stream = get_openai_response(
                prompt, 
                llm_system_massage_manager.get_first_system_prompt(filtered_df.to_markdown() if not filtered_df.empty else "אין נתונים זמינים"), 
                st.session_state.messages[:-1], 
                st.session_state.graph_data,
                stream=True
            )
            
            # לולאה על אירועי הסטרים והצגת התשובה בזמן אמת
            for chunk in response_stream:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        # מציג את התשובה המתעדכנת עם סמן מהבהב
                        message_placeholder.markdown(full_response + "▌")
            
            # הצגת התשובה המלאה הסופית (ללא הסמן)
            message_placeholder.markdown(full_response)
        
        # הוספת התשובה להיסטוריה
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Helper functions for sample graphs if no data is available
def generate_sample_gauge(value=3.7, title="חוסן"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 24}},
        gauge={
            'axis': {'range': [1, 5]},
            'bar': {'color': "#437742"},
            'steps': [
                {'range': [1, 2], 'color': "#f4f4f4"},
                {'range': [2, 3], 'color': "#f0f0f0"},
                {'range': [3, 4], 'color': "#e8e8e8"},
                {'range': [4, 5], 'color': "#e0e0e0"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 3.5
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def generate_sample_bar_chart():
    categories = ["קטגוריה א", "קטגוריה ב", "קטגוריה ג", "קטגוריה ד"]
    values = [4.2, 3.8, 2.5, 3.9]
    
    df = pd.DataFrame({"name": categories, "value": values})
    fig = px.bar(df, x='name', y='value', title="התפלגות ציונים")
    
    # Add reference lines
    fig.add_hline(y=3.5, line=dict(color="#F37321"), annotation_text="ממוצע מחקרי")
    fig.add_hline(y=3.2, line=dict(color="#1F3B91"), annotation_text="ממוצע ארצי")
    
    fig.update_layout(height=300)
    return fig

def generate_sample_spider():
    categories = ["תפיסת עבר מעכבת", "עבר כתשתית חיובית", "דטרמינסטיות",
                 "סיפוק מיידי", "עתיד"]
    
    fig = go.Figure()
    
    # Current values
    fig.add_trace(go.Scatterpolar(
        r=[3.2, 4.1, 2.8, 3.5, 3.9],
        theta=categories,
        fill='none',
        name='ממוצע נוכחי',
        line=dict(color='#437742')
    ))
    
    # Global average
    fig.add_trace(go.Scatterpolar(
        r=[3.0, 3.8, 3.0, 3.2, 3.7],
        theta=categories,
        fill='none',
        name='ממוצע ארצי',
        line=dict(color='#1F3B91')
    ))
    
    # Research average
    fig.add_trace(go.Scatterpolar(
        r=[2.8, 4.0, 2.5, 3.0, 4.0],
        theta=categories,
        fill='none',
        name='ממוצע מחקרי',
        line=dict(color='#F37321')
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
    
    return fig

# Run the main dashboard
if __name__ == "__main__":
    main()