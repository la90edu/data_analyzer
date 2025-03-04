import streamlit as st
import pandas as pd
import init
import compare_two_groups

df=init.init()

df_female = df[df['gender'] == 'female']
df_male=df[df['gender'] == 'male']
compare_two_groups.comare_two_groups_show_graphs(df_female,"נערות",df_male,"נערים")


# st.dataframe(df_female)
# st.dataframe(df_male)