"""
# השוואת בין מדדי למ"ס
"""

import streamlit as st
import pandas as pd
import init
import compare_multipul_groups
from class_school_info import SchoolInfo

df=init.init()

st.title('ניתוח למ"ס ')

#יוצר חלוקה לדאטא פריימס שונים ע"פ למס שונים
df_lamas_dict = {lamas: df[df['lamas'] == lamas] for lamas in df['lamas'].unique()}
compare_multipul_groups.show_comare_multipul_groups_lamas("מיקוד שליטה פנימית","ici",df_lamas_dict[2],"למ\"ס 2",df_lamas_dict[3],"למ\"ס 3",df_lamas_dict[4],"למ\"ס 4",df_lamas_dict[5],"למ\"ס 5",df_lamas_dict[6],"למ\"ס 6",df_lamas_dict[7],"למ\"ס 7")
compare_multipul_groups.show_comare_multipul_groups_lamas("חוסן","risc",df_lamas_dict[2],"למ\"ס 2",df_lamas_dict[3],"למ\"ס 3",df_lamas_dict[4],"למ\"ס 4",df_lamas_dict[5],"למ\"ס 5",df_lamas_dict[6],"למ\"ס 6",df_lamas_dict[7],"למ\"ס 7")



# unique_lamas = df["lamas"].unique().tolist()
unique_lamas = sorted(df["lamas"].unique().tolist())

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
lamas_that_was_chosen = st.selectbox('בחר', unique_lamas)
schoolInfo = SchoolInfo(df[df['lamas']==lamas_that_was_chosen])
fig_spider=schoolInfo.get_fig_spider()
st.plotly_chart(fig_spider, key="unique_key_spider", use_container_width=True)
# fig_ici=schoolInfo.get_fig_ici("ici")
# fig_risc=schoolInfo.get_fig_risc("risc")
# # יצירת שלוש עמודות
# col1, col2 = st.columns(2)
# # הצגת כל גרף בתוך עמודה משלו
# with col1:
#         st.plotly_chart(fig_ici, key="unique_key_ici", use_container_width=True)
# with col2:
#         st.plotly_chart(fig_risc, key="unique_key_risc", use_container_width=True)

    
# df=init.init()

# df_lamas_2=df[df['lamas'] == 2]
# df_lamas_3=df[df['lamas'] == 3]
# df_lamas_4=df[df['lamas'] == 4]
# df_lamas_5=df[df['lamas'] == 5]
# df_lamas_6=df[df['lamas'] == 6]
# df_lamas_7=df[df['lamas'] == 7]


# compare_multipul_groups.comare_multipul_groups(df_lamas_2,"למ\"ס 2",df_lamas_3,"למ\"ס 3",df_lamas_4,"למ\"ס 4",df_lamas_5,"למ\"ס 5",df_lamas_6,"למ\"ס 6",df_lamas_7,"למ\"ס 7")
# # compare_two_groups.comare_two_groups_show_graphs(df_female,"נערות",df_male,"נערים")


# st.dataframe(df_lamas_2)
# st.dataframe(df_lamas_3)
# st.dataframe(df_lamas_4)
# st.dataframe(df_lamas_5)
# st.dataframe(df_lamas_6)
# st.dataframe(df_lamas_7)
