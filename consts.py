import anigmas
import pandas as pd
import streamlit as st


colors = {
    "current_color": "#FF5733",
    "global_color": "#33FF57",
    "research_color": "#5733FF"
}

research_average={
    "ici":3.71,
    "risc":3.22,
    "future_negetive_past":2.47,
    "future_positive_past":3.2,
    "future_fatalic_present":2.7,
    "future_hedonistic_present":2.84,
    "future_future":3.68
    
}

def return_research_average():
    return research_average 

def init_st_session_global_average_and_research_average(global_df):
    # יצירת מילון global_average ישירות מהפונקציות של anigmas במקום שימוש ב-SchoolInfo
    global_average = {
        "ici": float(anigmas.ici_result(global_df)),
        "risc": float(anigmas.risc_result(global_df)),
        "future_negetive_past": float(anigmas.future_negetive_past_result(global_df)),
        "future_positive_past": float(anigmas.future_positive_past_result(global_df)),
        "future_fatalic_present": float(anigmas.future_fatalic_present_result(global_df)),
        "future_hedonistic_present": float(anigmas.future_hedonistic_present_result(global_df)),
        "future_future": float(anigmas.future_future_result(global_df))
    }
    # אתחול המשתנים ב-session_state
    st.session_state.global_average = global_average
    st.session_state.research_average = research_average
    
    

def return_global_average(df): 
    global_average={
        "ici":float(anigmas.ici_result(df)),
        "risc":float(anigmas.risc_result(df))
    }
    
    return global_average

def init_heg_avg(df):
    heg_avg=anigmas.get_global_heg_avg_as_dict(df)
    st.session_state.heg_avg=heg_avg
    return heg_avg