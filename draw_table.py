import pandas as pd
import streamlit as st
import anigmas


def draw_analyzed_table(df,table_name):
    
    
    st.write(f"### {table_name}")   
    
    data = [
    ["ici",anigmas.ici_result(df)["mean"] , anigmas.ici_result(df)["var"]], 
    ["risc",anigmas.risc_result(df)["mean"] , anigmas.risc_result(df)["var"]],
    ["future_negetive_past",anigmas.future_negetive_past_result(df)["mean"] , anigmas.future_negetive_past_result(df)["var"]],
    ["future_positive_past",anigmas.future_positive_past_result(df)["mean"] , anigmas.future_positive_past_result(df)["var"]],
    ["future_fatalic_present",anigmas.future_fatalic_present_result(df)["mean"] , anigmas.future_fatalic_present_result(df)["var"]],
    ["future_hedonistic_present",anigmas.future_hedonistic_present_result(df)["mean"] , anigmas.future_hedonistic_present_result(df)["var"]],
    ["future_future",anigmas.future_future_result(df)["mean"] , anigmas.future_future_result(df)["var"] ]
    ]
    

# יצירת DataFrame מהנתונים
    df = pd.DataFrame(data, columns=["anigma", "mean", "var"])
    st.dataframe(df)
    
    # text=llm_gpt.return_llm_answer(df)
    # st.write(text)