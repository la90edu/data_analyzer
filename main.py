import streamlit as st
import pandas as pd
import draw_table
import connect_to_google_sheet
import plotly.graph_objects as go
import consts
from class_school_info import SchoolInfo
import plotly

st.set_page_config(layout="wide")
st.title('ניתוח ציר מנטלי ')

#init data
data=connect_to_google_sheet.return_data()
df=pd.DataFrame(data)

#init global and research average
consts.init_st_session_global_average_and_research_average(df)


unique_schools = df["school"].unique().tolist()
school = st.selectbox('Select a school', unique_schools)

schoolInfo = SchoolInfo(df[df['school']==school])
fig_ici=schoolInfo.get_fig_ici("ici")
fig_risc=schoolInfo.get_fig_risc("risc")
fig_spider=schoolInfo.get_fig_spider()

# st.plotly_chart(fig_ici, key="unique_key_ici")
# st.plotly_chart(fig_risc, key="unique_key_risc")
# st.plotly_chart(fig_spider, key="unique_key_spider")

import streamlit as st

# יצירת שלוש עמודות
col1, col2,col3 = st.columns(3)

# הצגת כל גרף בתוך עמודה משלו
with col1:
    st.plotly_chart(fig_ici, key="unique_key_ici", use_container_width=True)

with col2:
    st.plotly_chart(fig_risc, key="unique_key_risc", use_container_width=True)

with col3:
    st.plotly_chart(fig_spider, key="unique_key_spider", use_container_width=True)

# school_mean=schoolInfo.ici_result_mean()
# school_fig=schoolInfo.get_fig_gauge("ici",school_mean, global_average['ici'], research_average['ici'])
# st.plotly_chart(school_fig)

# school_mean_risc=schoolInfo.risc_result_mean()
# school_fig_risc=schoolInfo.get_fig_gauge("risc",school_mean_risc, global_average['risc'], research_average['risc'])
# st.plotly_chart(school_fig_risc)


# draw_table.draw_analyzed_table(df[df['school']==school],school)
# print(df)


