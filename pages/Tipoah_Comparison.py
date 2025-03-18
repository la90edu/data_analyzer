"""
# השוואה בין ממדי טיפוח 
"""

import streamlit as st
import pandas as pd
import init
import compare_multipul_groups
from class_school_info import SchoolInfo

                                 


df = init.init()

st.title('ניתוח מדדי טיפוח ')

# יוצר חלוקה לדאטא פריימס שונים ע"פ למס שונים
df_tipoh_dict = {tipoh: df[df['tipoh'] == tipoh] for tipoh in df['tipoh'].unique()}

compare_multipul_groups.show_comare_multipul_groups_tipoh(
    "מיקוד שליטה פנימית", "ici",
    df_tipoh_dict[4], "טיפוח 4",
    df_tipoh_dict[5], "טיפוח 5",
    df_tipoh_dict[6], "טיפוח 6",
    df_tipoh_dict[7], "טיפוח 7",
    df_tipoh_dict[8], "טיפוח 8",
    df_tipoh_dict[9], "טיפוח 9",
    df_tipoh_dict[10], "טיפוח 10"
)

compare_multipul_groups.show_comare_multipul_groups_tipoh(
    "חוסן", "risc",
    df_tipoh_dict[4], "טיפוח 4",
    df_tipoh_dict[5], "טיפוח 5",
    df_tipoh_dict[6], "טיפוח 6",
    df_tipoh_dict[7], "טיפוח 7",
    df_tipoh_dict[8], "טיפוח 8",
    df_tipoh_dict[9], "טיפוח 9",
    df_tipoh_dict[10], "טיפוח 10"
)
#     tipoh: df[df['tipoh'] == tipoh] 
#     for tipoh in sorted(df['tipoh'].unique(), key=lambda x: float(x))
# }





unique = sorted(df["tipoh"].unique().tolist())

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
tipoh_that_was_chosen = st.selectbox('בחרו מדד טיפוח', unique)
schoolInfo = SchoolInfo(df[df['tipoh']==tipoh_that_was_chosen])
fig_spider=schoolInfo.get_fig_spider()
st.plotly_chart(fig_spider, key="tipoh_key_spider", use_container_width=True)
