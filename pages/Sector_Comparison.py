import streamlit as st
import pandas as pd
import init
import compare_two_groups

df=init.init()

non_jews_schools=["מקיף שש שנתי פקיעין - פקיעין (בוקייעה)","מקיף דרכא ג'וליס - ג'ולס"]

df_non_jews = df[df['school'].isin(non_jews_schools)]
df_jews = df[~df['school'].isin(non_jews_schools)]


compare_two_groups.comare_two_groups_show_graphs(df_jews,"יהודים",df_non_jews,"אינם יהודים")
# st.dataframe(df_jews)

