import streamlit as st
import pandas as pd
import consts
import connect_to_google_sheet
import texts


def init():
    st.set_page_config(
        layout="wide",
        page_title="דאשבורד ניתוח נתונים",
        page_icon="📊",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "אפליקציה לניתוח נתונים פסיכולוגיים של תלמידים"
        }
    )
    st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6 {
        text-align: right;
        direction: rtl;
    }

    .css-1d391kg { 
        text-align: right; 
    }
    p {
        text-align: right;
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True
)

   
    data=connect_to_google_sheet.return_data()
    df=pd.DataFrame(data)
    # st.session_state.df=df
    consts.init_st_session_global_average_and_research_average(df)
    consts.init_heg_avg(df)
    return df

#for selectbox 
# st.markdown(
#         """
#         <style>
#         div[data-testid="stSelectbox"] {
#                 text-align: right;
#                 direction: rtl;
#                 width: 150px; /* Reduced width from 200px to 150px */
#                 margin-left: auto;
#                 margin-right: 0;
#         }
#         div[data-testid="stSelectbox"] > label > p {
#                 text-align: right;
#                 direction: rtl;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
# )