import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

#makes a graph bar in plotly where this dict is the data and the line is a constant line
def draw_bar_chart(name, thisdict, research_line, research_line_name, global_line, global_line_name):
    df = pd.DataFrame(thisdict)

    fig = px.bar(df, x='name', y='value', title=name, labels={'name': 'המדד', 'value': 'ערך ממוצע'})
    fig.add_hline(y=research_line, line=dict(color="#F37321"))
    fig.add_hline(y=global_line, line=dict(color="#1F3B91"))
    # הוספת מקרא לline ו-line2:
    fig.add_trace(
        go.Scatter(
            x=[df['name'].iloc[0], df['name'].iloc[-1]],
            y=[research_line, research_line],
            mode='lines+text',
            name=f"{research_line_name} ({research_line:.3f})",
            text=[f"{research_line:.3f}", f"{research_line:.3f}"],
            textposition="top center",
            line=dict(color="#F37321")
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[df['name'].iloc[0], df['name'].iloc[-1]],
            y=[global_line, global_line],
            mode='lines+text',
            name=f"{global_line_name} ({global_line:.3f})",
            text=[f"{global_line:.3f}", f"{global_line:.3f}"],
            textposition="top center",
            line=dict(color="#1F3B91")
        )
    )
    fig.update_layout(title=dict(x=1, xanchor='right'))

    # st.plotly_chart(fig, use_container_width=True)
    return fig
