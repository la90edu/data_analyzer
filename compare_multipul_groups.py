import streamlit as st
import pandas as pd
from class_school_info import SchoolInfo
import plotly.graph_objects as go
import graph_manager

def comare_multipul_groups(df1,group1_name,df2,group2_name,df3,group3_name,df4,group4_name,df5,group5_name,df6,group6_name):
    
    dict1 = SchoolInfo(df1).return_anigmas_result_as_dict()
    dict2 = SchoolInfo(df2).return_anigmas_result_as_dict()
    dict3 = SchoolInfo(df3).return_anigmas_result_as_dict()
    dict4 = SchoolInfo(df4).return_anigmas_result_as_dict()
    dict5 = SchoolInfo(df5).return_anigmas_result_as_dict()
    dict6 = SchoolInfo(df6).return_anigmas_result_as_dict()
    
    bar_graph=graph_manager.Bar_Chart_Graph_type("ici","ici",dict1,group1_name,dict2,group2_name,dict3,group3_name,dict4,group4_name,dict5,group5_name,dict6,group6_name) 
    
    # fig_ici1=schoolInfo1.get_fig_ici("ici")
    # fig_risc1=schoolInfo1.get_fig_risc("risc")
    # fig_spider1=schoolInfo1.get_fig_spider()
    
    # schoolInfo2 = SchoolInfo(df2)
    # fig_ici2=schoolInfo2.get_fig_ici("ici")
    # fig_risc2=schoolInfo2.get_fig_risc("risc")  
    # fig_spider2=schoolInfo2.get_fig_spider()
    
    # # יצירת שלוש עמודות
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.title(group1_name)
    #     st.plotly_chart(fig_ici1, key="unique_key_ici1", use_container_width=True)
    #     st.plotly_chart(fig_risc1, key="unique_key_risc1", use_container_width=True)
    #     st.plotly_chart(fig_spider1, key="unique_key_spider1", use_container_width=True)
    # with col2:
    #     st.title(group2_name)
    #     st.plotly_chart(fig_ici2, key="unique_key_ici2", use_container_width=True)
    #     st.plotly_chart(fig_risc2, key="unique_key_risc2", use_container_width=True)
    #     st.plotly_chart(fig_spider2, key="unique_key_spider2", use_container_width=True)
    