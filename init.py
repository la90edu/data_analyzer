import streamlit as st
import pandas as pd
import consts
import connect_to_google_sheet

def init():
    st.set_page_config(layout="wide")
    st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6 {
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
    return df