import streamlit as st
import pandas as pd
import init
import compare_two_groups

df=init.init()

df_class_8 = df[df['class'] == 'class_8']
df_class_10=df[df['class'] == 'class_10']
compare_two_groups.comare_two_groups_show_graphs(df_class_8,"כיתה ח'",df_class_10,"כיתה י'")


st.dataframe(df_class_8)
st.dataframe(df_class_10)