import streamlit as st
import pandas as pd
import draw_table
import connect_to_google_sheet
import plotly.graph_objects as go
import consts
from class_school_info import SchoolInfo
import plotly
import init
import chatbot_ex

# st.set_page_config(page_title="ניתוח על פי בית ספר")
# st.session_state.is_schhol_selected=False


# st.set_page_config(page_title="ניתוח על פי בית ספר", layout="wide")
df=init.init()
st.title('ניתוח ציר מנטלי ')



# if (st.session_state.is_schhol_selected==False):
unique_schools = df["school"].unique().tolist()
school = st.selectbox('בחר בית ספר', unique_schools)
    # if school :
    #     st.session_state.is_schhol_selected=True
    #     st.session_state.school=school

# if st.session_state.is_schhol_selected:
#     school = st.session_state.school
school_info = SchoolInfo(df[df['school']==school])
fig_ici=school_info.get_fig_ici("ici")
fig_risc=school_info.get_fig_risc("risc")
fig_spider=school_info.get_fig_spider()

# st.dataframe(pd.DataFrame(school_info.return_delta_from_global_as_dict()))

# Split the page into two columns
col1, col2 = st.columns([2, 1])

# First row: Three graphs side by side
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_ici, key="unique_key_ici", use_container_width=True)
with col2:
    st.plotly_chart(fig_risc, key="unique_key_risc", use_container_width=True)
with col3:
    st.plotly_chart(fig_spider, key="unique_key_spider", use_container_width=True)

# Second row: Chatbot spanning full width
st.markdown("<br>", unsafe_allow_html=True)
chatbot_container = st.container()
with chatbot_container:
    chatbot_ex.put_chatbot(df[df['school'] == school])



