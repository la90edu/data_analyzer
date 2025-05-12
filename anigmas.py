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

def cut_df_from_dictionary(dict,anigma_name):
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
                
    dict_cuted = {k: dict[k] for k in cols}
    return dict_cuted

def return_wrost_heg_from_anigma_acoording_to_delta_from_global(df,anigma_name):
    current_df_cuted=cut_df(df,anigma_name)
    current_mean = current_df_cuted.mean()
    current_mean_dict = current_mean.to_dict()
    
    global_mean_dict=cut_df_from_dictionary(st.session_state.heg_avg,anigma_name)
    
    key=return_biggest_delta_from_global(current_mean_dict,global_mean_dict)[0]
    value=return_biggest_delta_from_global(current_mean_dict,global_mean_dict)[1]
    
    return_second_biggest_delta_from_global(current_mean_dict,global_mean_dict,key)
    
    # st.write(f"chosen anigma:{anigma_name}")
    # st.write(f"current mean: {current_mean_dict}")
    # st.write(f"global mean: {global_mean_dict}")
    
    

def get_precentage_delta(global_,local):
        
        delta=(global_-local)/global_
        return delta
        
def return_biggest_delta_from_global(local_dict,global_dict):
        delta_dict={}
        for key in local_dict.keys():
            delta=get_precentage_delta(global_dict[key],local_dict[key])
            delta_dict[key]=delta
        
        #finds the max key from the delta dict
        max_key = max(delta_dict, key=delta_dict.get)
        max_value = delta_dict[max_key]
        
        # st.write("local dict:")
        # st.write(local_dict)
        # st.write("global dict:")
        # st.write(global_dict)
        # st.write("delta dict:")
        # st.write(delta_dict)
        # st.write(f"max key: {max_key}")
        # st.write(f"max value: {max_value}")
        return max_key,max_value
    
def return_second_biggest_delta_from_global(local_dict,global_dict,biggest_key):
        delta_dict={}
        for key in local_dict.keys():
            if key != biggest_key:
                delta=get_precentage_delta(global_dict[key],local_dict[key])
                delta_dict[key]=delta
        
        #finds the max key from the delta dict
        max_key = max(delta_dict, key=delta_dict.get)
        max_value = delta_dict[max_key]
        
        return max_key,max_value
        
        
def return_first_and_second_heg_for_worst_heg(df,anigma_name):
    current_df_cuted=cut_df(df,anigma_name)
    current_mean = current_df_cuted.mean()
    current_mean_dict = current_mean.to_dict()
    
    global_mean_dict=cut_df_from_dictionary(st.session_state.heg_avg,anigma_name)
    
    key=return_biggest_delta_from_global(current_mean_dict,global_mean_dict)[0]
    value=return_biggest_delta_from_global(current_mean_dict,global_mean_dict)[1]
    
    key2,value2=return_second_biggest_delta_from_global(current_mean_dict,global_mean_dict,key)
    
    # st.write(f"chosen anigma:{anigma_name}")
    # st.write(f"current mean: {current_mean_dict}")
    # st.write(f"global mean: {global_mean_dict}")
    
    # st.write(f"worst heg: {key} with value: {value}")
    # st.write(f"second worst heg: {key2} with value: {value2}")
    
    return key,value,key2,value2
    
    
    
    
    
    

def get_max_average_higed_from_anigma(df,anigma_name):
    df_cuted=cut_df(df,anigma_name)
    result=actions.return_sum_dict(df_cuted)
    # st.write(f"chosen anigma:{anigma_name}")
    # st.write(result)
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
    

def get_global_heg_avg_as_dict(df):
    cols=('heg_1','heg_2','heg_3','heg_4','heg_5','heg_6','heg_7','heg_8','heg_9',
                'heg_10','heg_11','heg_12','heg_13','heg_14','heg_15','heg_16',
                'heg_17','heg_18','heg_19','heg_21','heg_22','heg_23','heg_24',
                'heg_25','heg_26','heg_27')
    df_heg = df.filter(items=cols)
    #יוצר שורה חדשה עם ממוצע של כל עמודה 
    df_heg.loc['average'] = df_heg.mean() 
    #מעביר את שורת הממוצע לdictonary
    heg_dict = df_heg.loc['average'].to_dict()
    
    return heg_dict
