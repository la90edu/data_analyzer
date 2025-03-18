import plotly.graph_objects as go
import streamlit as st

def dict_to_list(dict):
    lst=[]
    lst.append(dict["future_negetive_past"])
    lst.append(dict["future_positive_past"])
    lst.append(dict["future_fatalic_present"])
    lst.append(dict["future_hedonistic_present"])
    lst.append(dict["future_future"])
    return lst

def draw_spider_graph(name, current_averages, global_averages, research_averagers):
    lst_current = dict_to_list(current_averages)
    lst_global = dict_to_list(global_averages)
    lst_research = dict_to_list(research_averagers)

    categories = ["תפיסת עבר מעכבת", "עבר כתשתית חיובית", "דטרמינסטיות",
                  "סיפוק מיידי", "עתיד"]

    fig = go.Figure()

    
    fig.add_trace(go.Scatterpolar(
        r=lst_current,
        theta=categories,
        fill='none',
        name='ממוצע נוכחי',
        line=dict(color='#437742')  # צבע ייחודי למקרא
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=lst_global,
        theta=categories,
        fill='none',
        name='ממוצע ארצי',
        line=dict(color='#1F3B91')  # צבע ייחודי למקרא
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=lst_research,
        theta=categories,
        fill='none',
        name='ממוצע מחקרי ',
        line=dict(color='#F37321')  # צבע ייחודי למקרא
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[1, 5]
            )
        ),
        showlegend=True  # ✅ הצגת המקרא
    )

    return fig

# categories = ['processing cost','mechanical properties','chemical stability',
#               'thermal stability', 'device integration']

# fig = go.Figure()

# fig.add_trace(go.Scatterpolar(
#       r=[1, 5, 2, 2, 3],
#       theta=categories,
#       fill='toself',
#       name='Product A'
# ))
# fig.add_trace(go.Scatterpolar(
#       r=[4, 3, 2.5, 1, 2],
#       theta=categories,
#       fill='toself',
#       name='Product B'
# ))
# fig.add_trace(go.Scatterpolar(
#       r=[3, 2, 2.5, 4, 5],
#       theta=categories,
#       fill='toself',
#       name='Product C'
# ))

# fig.update_layout(
#   polar=dict(
#     radialaxis=dict(
#       visible=True,
#       range=[0, 5]
#     )),
#   showlegend=False
# )
