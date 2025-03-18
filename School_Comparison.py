"""
# ניתוח על פי בית ספר
# """

import streamlit as st
import pandas as pd
import draw_table
import connect_to_google_sheet
import plotly.graph_objects as go
import consts
from class_school_info import SchoolInfo
import plotly
import init

df=init.init()
st.title('ניתוח ציר מנטלי ')

unique_schools = df["school"].unique().tolist()
st.markdown(
        """
        <style>
        div[data-testid="stSelectbox"] {
                text-align: right;
                direction: rtl;
                width: 150px; /* Reduced width from 200px to 150px */
                margin-left: auto;
                margin-right: 0;
        }
        div[data-testid="stSelectbox"] > label > p {
                text-align: right;
                direction: rtl;
        }
        </style>
        """,
        unsafe_allow_html=True
)

school = st.selectbox('בחר בית ספר', unique_schools)

school_info = SchoolInfo(df[df['school']==school])
fig_ici=school_info.get_fig_ici("ici")
fig_risc=school_info.get_fig_risc("risc")
fig_spider=school_info.get_fig_spider()

# st.dataframe(pd.DataFrame(school_info.return_delta_from_global_as_dict()))


# הצגת הגרפים במרכז, אחד מתחת לשני עם פחות רווח
st.plotly_chart(fig_ici, key="unique_key_ici", use_container_width=True)
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.plotly_chart(fig_risc, key="unique_key_risc", use_container_width=True)
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.plotly_chart(fig_spider, key="unique_key_spider", use_container_width=True)
    

# school_mean=schoolInfo.ici_result_mean()
# school_fig=schoolInfo.get_fig_gauge("ici",school_mean, global_average['ici'], research_average['ici'])
# st.plotly_chart(school_fig)

# school_mean_risc=schoolInfo.risc_result_mean()
# school_fig_risc=schoolInfo.get_fig_gauge("risc",school_mean_risc, global_average['risc'], research_average['risc'])
# st.plotly_chart(school_fig_risc)


# draw_table.draw_analyzed_table(df[df['school']==school],school)
# print(df)


