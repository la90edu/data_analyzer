import pandas as pd
import actions
import streamlit as st

def cut_df(df,anigma_name):
   match anigma_name:
        case "ici":
            cols=('heg_1','heg_5','heg_10','heg_12','heg_24','heg_26')
        case "risc":
            cols=("heg_4","heg_14","heg_18","heg_19")
        case "future_negetive_past":
            cols=('heg_2','heg_13','heg_23')
        case "future_positive_past":
            cols=('heg_6','heg_16','heg_21')
        case "future_fatalic_present":
            cols=('heg_3','heg_15','heg_22')
        case "future_hedonistic_present":
            cols=('heg_11','heg_17','heg_25')
        case "future_future":
            cols=('heg_7','heg_8','heg_9','heg_27')
        case _:
            print("anigma name not found")
            
   df_cuted = df.filter(items=cols)
   return df_cuted

def get_max_average_higed_from_anigma(df,anigma_name):
    df_cuted=cut_df(df,anigma_name)
    result=actions.return_sum_dict(df_cuted)
    st.write(f"chosen anigma:{anigma_name}")
    st.write(result)
    st.dataframe(df)
    return result


            
             
    
def ici_result(df):
    ici_cols=('heg_1','heg_5','heg_10','heg_12','heg_24','heg_26')
    df_ici = df.filter(items=ici_cols)
    return actions.return_mean_from_df(df_ici)

def risc_result(df):
    risc_cols=("heg_4","heg_14","heg_18","heg_19")
    df_risc=df.filter(items=risc_cols)
    return actions.return_mean_from_df(df_risc)

def future_negetive_past_result(df):
    future_negetive_past_cols=('heg_2','heg_13','heg_23')
    df_future_negetive_past=df.filter(items=future_negetive_past_cols)
    return actions.return_mean_from_df(df_future_negetive_past)

def future_positive_past_result(df):
    future_positive_past_cols=('heg_6','heg_16','heg_21')
    df_future_positive_past=df.filter(items=future_positive_past_cols)
    return actions.return_mean_from_df(df_future_positive_past)

def future_fatalic_present_result(df):
    future_fatalic_present_cols=('heg_3','heg_15','heg_22')
    df_future_fatalic_present=df.filter(items=future_fatalic_present_cols)
    return actions.return_mean_from_df(df_future_fatalic_present)

def future_hedonistic_present_result(df):
    future_hedonistic_present_cols=('heg_11','heg_17','heg_25')
    df_future_hedonistic_present=df.filter(items=future_hedonistic_present_cols)
    return actions.return_mean_from_df(df_future_hedonistic_present)

def future_future_result(df):
    future_future_cols=('heg_7','heg_8','heg_9','heg_27')
    df_future_future=df.filter(items=future_future_cols)
    return actions.return_mean_from_df(df_future_future)
    

