import streamlit as st
import pandas as pd
import init
import compare_multipul_groups
from class_school_info import SchoolInfo

df=init.init()

st.title('ניתוח מדדי טיפוח  ')

unique_lamas = df["tipoh"].unique().tolist()
chosen = st.selectbox('Select tipoh sector', unique_lamas)

schoolInfo = SchoolInfo(df[df['tipoh']==chosen])
fig_ici=schoolInfo.get_fig_ici("ici")
fig_risc=schoolInfo.get_fig_risc("risc")
fig_spider=schoolInfo.get_fig_spider()



# יצירת שלוש עמודות
col1, col2 = st.columns(2)
# הצגת כל גרף בתוך עמודה משלו
with col1:
        st.plotly_chart(fig_ici, key="unique_key_ici", use_container_width=True)
with col2:
        st.plotly_chart(fig_risc, key="unique_key_risc", use_container_width=True)

st.plotly_chart(fig_spider, key="unique_key_spider", use_container_width=True)
    


# import streamlit as st
# import pandas as pd
# import init
# import compare_multipul_groups
# from class_school_info import SchoolInfo

# df=init.init()

# st.title("ניתוח על פי מדד טיפוח" )

# unique_tipoh = df["tipoh"].unique().tolist()
# tipoh_that_was_chosen = st.selectbox('Select tipoh sector', unique_tipoh)
# st.dataframe(df[df['tipoh']==tipoh_that_was_chosen])
# schoolInfo = SchoolInfo(df[df['lamas']==tipoh_that_was_chosen])
# fig_ici=schoolInfo.get_fig_ici("ici")
# fig_risc=schoolInfo.get_fig_risc("risc")
# fig_spider=schoolInfo.get_fig_spider()




# # יצירת שלוש עמודות
# col1, col2 = st.columns(2)
# # הצגת כל גרף בתוך עמודה משלו
# with col1:
#         st.plotly_chart(fig_ici, key="unique_key_ici", use_container_width=True)
# with col2:
#         st.plotly_chart(fig_risc, key="unique_key_risc", use_container_width=True)

# st.plotly_chart(fig_spider, key="unique_key_spider", use_container_width=True)
