import anigmas
import pandas as pd
from class_school_info import SchoolInfo
import streamlit as st


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
    global_average=SchoolInfo(global_df).return_anigmas_result_as_dict()
    st.session_state.global_average=global_average
    st.session_state.research_average=research_average
    
    

def return_global_average(df): 
    global_average={
        "ici":float(anigmas.ici_result(df)),
        "risc":float(anigmas.risc_result(df))
    }
    
    return global_average