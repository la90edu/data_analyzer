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
        margin-top: 1rem; /* מרווח מלמעלה למניעת חפיפה עם הכותרות */
    }
    
    /* כותרות גרפים */
    .graph-title {
        margin-bottom: 15px; /* מרווח בין הכותרת לגרף */
        padding-top: 10px; /* מרווח בין הכותרת לגרף */
    }
    
    /* Fix headers position to prevent overlap */
    h3 {
        margin-bottom: 0.8rem !important;
        padding-top: 0.5rem !important;
        line-height: 1.6 !important;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    /* Sidebar styling - הגבלת רוחב ה-sidebar */
    [data-testid="stSidebar"] {
        min-width: 200px !important;
        max-width: 200px !important;
        width: 200px !important;
    }
    
    /* ביטול מרווחים מיותרים בסרגל הצד */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
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
    
    /* Fix container heights to prevent overlap */
    [data-testid="stVerticalBlock"] {
        gap: 1rem !important;
    }
    
    /* Sidebar styling לקלאס הקודם */
    .css-1d391kg {
        text-align: right;
        direction: rtl;
    }
    
    /* Selectbox RTL support */
    div[data-testid="stSelectbox"] {
        text-align: right;
        direction: rtl;
    }
    
    div[data-testid="stSelectbox"] > label > p {
        text-align: right;
        direction: rtl;
    }
    
    /* Make sure markdown in chat messages appears correctly in RTL */
    .element-container .stMarkdown {
        direction: rtl;
        text-align: right;
    }
    
    /* Styling for markdown elements in chat */
    .element-container .stMarkdown h1,
    .element-container .stMarkdown h2,
    .element-container .stMarkdown h3,
    .element-container .stMarkdown h4,
    .element-container .stMarkdown h5,
    .element-container .stMarkdown h6,
    .element-container .stMarkdown p,
    .element-container .stMarkdown ul,
    .element-container .stMarkdown ol {
        direction: rtl;
        text-align: right;
    }
    
    /* התאמה למובייל - Media Queries */
    @media (max-width: 768px) {
        /* הקטנת כותרות במובייל */
        h1 {
            font-size: 1.8rem !important;
        }
        h2, h3 {
            font-size: 1.4rem !important;
            margin-bottom: 1rem !important;
            padding-top: 0.8rem !important;
        }
        
        /* צמצום מרווחים במובייל */
        .main .block-container {
            padding: 1rem 0.5rem !important;
        }
        
        /* התאמת הגרפים למובייל */
        .stPlotlyChart {
            padding: 5px;
            margin-bottom: 0.5rem;
            margin-top: 1.2rem; /* יותר מרווח במובייל */
        }
        
        /* שינוי פריסה במובייל - גרפים בטור ולא בשורה */
        @media (max-width: 640px) {
            [data-testid="column"] {
                min-width: 100% !important;
                width: 100% !important;
                margin-bottom: 1rem;
            }
        }
        
        /* התאמת הסיידבר למובייל - רוחב מוקטן */
        [data-testid="stSidebar"] {
            min-width: 160px !important;
            max-width: 160px !important;
            width: 160px !important;
        }
        
        /* התאמת גודל כפתורים וטקסט במובייל */
        button {
            font-size: 0.8rem !important;
            padding: 0.3rem !important;
        }
        
        /* התאמת תיבת צ'אט למובייל */
        .chat-container {
            padding: 10px;
        }
        
        /* מרווחים בין המיכלים במובייל */
        [data-testid="stVerticalBlock"] {
            gap: 1.5rem !important;
        }
    }

    /* התאמות נוספות למסכים קטנים מאוד */
    @media (max-width: 480px) {
        /* גרפים עוד יותר קומפקטיים */
        .stPlotlyChart > div {
            height: 250px !important;
        }
        
        /* הקטנה נוספת של הכותרות */
        h1 {
            font-size: 1.5rem !important;
        }
        h2, h3 {
            font-size: 1.2rem !important;
            margin-bottom: 1.2rem !important;
            padding-top: 1rem !important;
        }
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

# Main Dashboard
def main():
    st.title("דאשבורד ניתוח נתונים 📊")
    st.markdown("### ניתוח נתונים חינוכיים עם גרפים ואינטראקציה")
    
    # הוספת גילוי מובייל
    is_mobile = False
    # לבדוק את רוחב המסך עם JavaScript (יודגם בצד הלקוח)
    st.markdown(
        """
        <script>
            if (window.innerWidth < 768) {
                document.documentElement.style.setProperty('--mobile-view', 'true');
            }
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # Load data
    try:
        df = init()
    except Exception as e:
        st.error(f"Aירעה שגיאה בטעינת הנתונים: {e}")
        df = pd.DataFrame()  # Empty dataframe as fallback
    
    # Sidebar for filtering
    with st.sidebar:
        st.header("סינון נתונים")
        
        # School selection
        selected_school = None
        if not df.empty and 'school' in df.columns:
            unique_schools = df["school"].unique().tolist()
            selected_school = st.selectbox("בחר בית ספר:", unique_schools)
            filtered_df = df[df['school'] == selected_school]
            st.session_state.graph_data["selected_school"] = selected_school
        else:
            # Demo data if no real data is available
            filtered_df = df
            st.warning("לא נמצאו נתונים לסינון")
    
    # בדיקה מובייל - אם רוחב המסך קטן מ-768px, נציג את הגרפים אחד מתחת לשני
    # החלפת הפונקציה המיושנת לפונקציה החדשה
    screen_width = st.query_params.get("width", ["1200"])[0]
    is_mobile = int(screen_width) < 768
    
    if is_mobile:
        # במובייל - כל גרף בקולונה נפרדת אחד מתחת לשני
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
            # שינוי שיטת הצגת הכותרת למניעת חפיפה
            st.markdown('<div class="graph-title"><h3>מדד חוסן</h3></div>', unsafe_allow_html=True)
            height = 250 if is_mobile else 300
            fig1 = generate_sample_gauge()
            # עדכון גובה הגרף ומרחק מהכותרת
            fig1.update_layout(height=height, margin=dict(t=30, b=10))
            st.plotly_chart(fig1, use_container_width=True)
            
            # שמירת נתוני גרף לדוגמה לצ'אטבוט
            st.session_state.graph_data["risc"] = {
                "value": 3.7,
                "global_avg": 3.5,
                "research_avg": 3.8
            }
            
        with row1_col2:
            # שינוי שיטת הצגת הכותרת למניעת חפיפה
            st.markdown('<div class="graph-title"><h3>מיקוד שליטה פנימי</h3></div>', unsafe_allow_html=True)
            height = 250 if is_mobile else 300
            fig2 = generate_sample_gauge(value=3.4, title="מיקוד שליטה פנימי")
            # עדכון גובה הגרף ומרחק מהכותרת
            fig2.update_layout(height=height, margin=dict(t=30, b=10))
            st.plotly_chart(fig2, use_container_width=True)
            
            # שמירת נתוני גרף לדוגמה לצ'אטבוט
            st.session_state.graph_data["ici"] = {
                "value": 3.4,
                "global_avg": 3.2,
                "research_avg": 3.6
            }
            
        with row1_col3:
            # שינוי שיטת הצגת הכותרת למניעת חפיפה
            st.markdown('<div class="graph-title"><h3>נתוני ציר הזמן</h3></div>', unsafe_allow_html=True)
            height = 250 if is_mobile else 300
            fig3 = generate_sample_spider()
            # עדכון גובה הגרף ומרחק מהכותרת
            fig3.update_layout(height=height, margin=dict(t=30, b=10))
            st.plotly_chart(fig3, use_container_width=True)
            
            # שמירת נתוני גרף לדוגמה לצ'אטבוט
            st.session_state.graph_data["spider"] = {
                "negetive_past": {"current": 3.2, "global": 3.0, "research": 2.8},
                "positive_past": {"current": 4.1, "global": 3.8, "research": 4.0},
                "fatalic_present": {"current": 2.8, "global": 3.0, "research": 2.5},
                "hedonistic_present": {"current": 3.5, "global": 3.2, "research": 3.0},
                "future": {"current": 3.9, "global": 3.7, "research": 4.0},
            }
    else:
        # Real graphs from data
        try:
            school_info = SchoolInfo(filtered_df)
            
            with row1_col1:
                # שינוי שיטת הצגת הכותרת למניעת חפיפה
                st.markdown('<div class="graph-title"><h3>מדד חוסן</h3></div>', unsafe_allow_html=True)
                # התאמת גובה הגרף למסך מובייל
                height = 250 if is_mobile else 300
                fig_risc = school_info.get_fig_risc("חוסן")
                # עדכון גובה הגרף ומרחק מהכותרת
                fig_risc.update_layout(height=height, margin=dict(t=30, b=10))
                st.plotly_chart(fig_risc, use_container_width=True)
                
                # שמירת נתוני גרף אמיתיים לצ'אטבוט
                st.session_state.graph_data["risc"] = {
                    "value": school_info.risc,
                    "global_avg": st.session_state.global_average["risc"],
                    "research_avg": st.session_state.research_average["risc"]
                }
                
            with row1_col2:
                # שינוי שיטת הצגת הכותרת למניעת חפיפה
                st.markdown('<div class="graph-title"><h3>מיקוד שליטה פנימי</h3></div>', unsafe_allow_html=True)
                # התאמת גובה הגרף למסך מובייל
                height = 250 if is_mobile else 300
                fig_ici = school_info.get_fig_ici("מיקוד שליטה")
                # עדכון גובה הגרף ומרחק מהכותרת
                fig_ici.update_layout(height=height, margin=dict(t=30, b=10))
                st.plotly_chart(fig_ici, use_container_width=True)
                
                # שמירת נתוני גרף אמיתיים לצ'אטבוט
                st.session_state.graph_data["ici"] = {
                    "value": school_info.ici,
                    "global_avg": st.session_state.global_average["ici"],
                    "research_avg": st.session_state.research_average["ici"]
                }
                
            with row1_col3:
                # שינוי שיטת הצגת הכותרת למניעת חפיפה
                st.markdown('<div class="graph-title"><h3>התפלגות לפי ממדי זמן</h3></div>', unsafe_allow_html=True)
                # התאמת גובה הגרף למסך מובייל
                height = 250 if is_mobile else 300
                fig_spider = school_info.get_fig_spider()
                # עדכון גובה הגרף ומרחק מהכותרת
                fig_spider.update_layout(height=height, margin=dict(t=30, b=10))
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
        except Exception as e:
            st.error(f"שגיאה בעת יצירת הגרפים: {e}")
    
    # Divider
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
    
    # התאמת כמות העמודות בהתאם לרוחב המסך
    col_count = 1 if is_mobile else 3
    cols = st.columns(col_count)
    for i, question in enumerate(suggested_questions):
        col_idx = i % col_count
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