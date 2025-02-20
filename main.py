import streamlit as st
import pandas as pd
import draw_table
import connect_to_google_sheet

data=connect_to_google_sheet.return_data()
df=pd.DataFrame(data)

draw_table.draw_analyzed_table(df,'master')

unique_schools = df["school"].unique().tolist()
school = st.selectbox('Select a school', unique_schools)

st.dataframe(df[df['school']==school])
draw_table.draw_analyzed_table(df[df['school']==school],school)
# print(df)
