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

    categories = ["התמקדות בחוויות טראומתיות מהעבר", "התמקדות בזכרונות חיוביים מהעבר", "תחושה של חוסר שליטה על העתיד",
                  "חיים והתמקדות בהווה ובהנאות של כאן ועכשיו גם במחיר ויתור על העתיד", "תכנון לטווח הארוך והסתכלות קדימה"]

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

    # הגדרות מעודכנות לתאימות טובה יותר למובייל
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[1, 5]
            )
        ),
        showlegend=True,  # הצגת המקרא
        legend=dict(
            orientation="h",  # מקרא אופקי במקום אנכי
            yanchor="bottom",
            y=-0.15,  # הזזת המקרא מתחת לגרף
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=10, r=10, t=30, b=80),  # שוליים מוקטנים
        height=550,  # גובה מוגדל לגרף
        autosize=True,  # תמיכה בשינוי גודל אוטומטי
    )

    return fig

# מוסיף פונקציית גרסה מוקטנת יותר לתצוגה במובייל
def draw_spider_graph_mobile(name, current_averages, global_averages, research_averagers):
    """גרסה מותאמת למובייל של גרף העכביש עם גודל ופרופורציות מותאמות למסכים קטנים"""
    
    fig = draw_spider_graph(name, current_averages, global_averages, research_averagers)
    
    # התאמות ספציפיות למובייל
    fig.update_layout(
        height=480,  # גובה מוגדל
        margin=dict(l=5, r=5, t=20, b=70),  # שוליים מותאמים לגרף גבוה יותר
        legend=dict(
            font=dict(size=10),  # טקסט מקרא קטן יותר
            y=-0.12,  # מיקום מעודכן של המקרא
        ),
        polar=dict(
            angularaxis=dict(
                tickfont=dict(size=9)  # גופן מעט גדול יותר לצירים
            )
        ),
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
