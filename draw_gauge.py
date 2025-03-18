import plotly.graph_objects as go
import streamlit as st 
import numpy as np


def draw_graph_gauge(name, value, avg_global, avg_research):
    
     
    # יצירת גרף
    fig = go.Figure(go.Indicator(
        mode="gauge", # הסרנו את ה-number כדי לשלוט במיקום שלו ידנית
        value=value,
        title={'text': f"<b>{name}</b>", 'font': {'size': 24}},
        gauge={
               'axis': {
                'range': [1, 5],
                'tickwidth': 1,           # עובי השנתות
                'tickcolor': "#888888",  # צבע השנתות
                'ticklen': 15,            # אורך השנתות - גדול יותר
                'tickmode': "array",      # מאפשר לקבוע ערכים ספציפיים
                'tickvals': [1, 2, 3, 4, 5],
                'ticktext': ["1", "2", "3", "4", "5"],
                'tickangle': 0,
                'tickfont': {'size': 14, 'color': 'black'},
                'ticklabelstep': 1,
                'showticklabels': True
            },
            'steps': [
                {'range': [avg_global - 0.05, avg_global + 0.05], 'color': '#1F3B91'},
                {'range': [avg_research - 0.05, avg_research + 0.05], 'color': '#F37321'}
            ],
            'bar': {'color': '#437742', 'thickness': 0.5}
        }
    ))
    
    
    # הוספת מקרא מותאם אישית
    legend_items = [
        {'color': '#1F3B91', 'label': f'{avg_global:.2f} :   ממוצע ארצי'},
        {'color': '#F37321', 'label': f'{avg_research} :ממוצע מחקרי'}
    ]
    
    #  מיקום התחלתי של המקרא
    legend_x = 0.95
    legend_y = 1.0  # Increased from 0.95 to 1.0
    circle_radius = 0.012 # רדיוס העיגול במקרא

    
    for item in legend_items: # הוספת עיגול צבעוני במקום ריבוע
        fig.add_shape(type="circle", 
                      x0=legend_x - circle_radius, 
                      y0=legend_y - circle_radius, 
                      x1=legend_x + circle_radius, 
                      y1=legend_y + circle_radius, 
                      line=dict(width=0, color='rgba(0,0,0,0)'), # ללא קו מתאר 
                      fillcolor=item['color'], xref='paper', yref='paper')

        # הוספת טקסט צמוד לעיגול - מרוחק קצת יותר
        fig.add_annotation(x=legend_x - 0.025, y=legend_y,  # הגדלת המרחק מ-0.02 ל-0.025
                          text=item['label'], showarrow=False,
                          font=dict(size=12, color="black"),
                          xanchor='right', yanchor='middle',
                          xref='paper', yref='paper')

        # עדכון מיקום ה-y עבור הפריט הבא במקרא
        legend_y -= 0.08  # רווח גדול יותר בין שורות המקרא


    
    # הוספת מחוון (needle) שמצביע על הערך הנוכחי
    # חישוב זווית המחוון בהתבסס על הערך
    min_value = 1
    max_value = 5
    angle = (value - min_value) / (max_value - min_value) * 180 - 90  # מעלות (מ -90 עד 90)
    
    # המרה מזווית לקואורדינטות
    angle_rad = np.radians(angle)
    x_head = 0.5 + 0.4 * np.cos(angle_rad)  # 0.5 הוא מרכז התרשים, 0.4 הוא אורך המחוון
    y_head = 0.5 + 0.4 * np.sin(angle_rad)  # 0.5 הוא מרכז התרשים
    
    # # הוספת קו המחוון
    # fig.add_shape(type="line",
    #               x0=0.5, y0=0.5,  # נקודת התחלה (מרכז הגרף)
    #               x1=x_head, y1=y_head,  # נקודת סיום (קצה המחוון)
    #               line=dict(color="red", width=4),
    #               xref="paper", yref="paper")
    
    # # הוספת עיגול במרכז המחוון
    # fig.add_shape(type="circle",
    #               x0=0.48,
    #               y0=0.20, 
    #               x1=0.52,
    #               y1=0.24,
    #               fillcolor="#ed1941",
    #               line_color="#ed1941",
    #               xref="paper", yref="paper")
    
    # הוספת הערך כמספר מתחת לעיגול האדום
    fig.add_annotation( 
        x=0.5,
        y=0.01, # מיקום למטה 
        text=f"{value:.2f}", 
        showarrow=False, 
        font=dict( 
            size=28, # גודל קטן יותר מהגודל המקורי 
            color="black", family="Arial", weight="bold" ), 
        xref="paper", 
        yref="paper" )

    # עדכון גובה הגרף לתצוגה טובה יותר
    fig.update_layout(height=400)
    
    # הצגת הגרף
    return fig





# def draw_graph_gauge_old(name,value,avg_national,avg_research):
# # נתונים
# # value = 3.7  
# # avg_national = 3.5  
# # avg_research = 4.0  

 
# # יצירת גרף
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=value,
#         title={'text': f"<b>{name}</b>", 'font': {'size': 24}},
#         gauge={
#             'axis': {'range': [1, 5]},
#             'steps': [
#                 {'range': [avg_national - 0.05, avg_national + 0.05], 'color': "blue"},
#                 {'range': [avg_research - 0.05, avg_research + 0.05], 'color': "orange"}
#             ],
#             'bar': {'color': "green", 'thickness': 0.3}
#         }
#     ))
    
#     # # הוספת margin ב-layout
#     # fig.update_layout(
#     # title={
#     #     'text': f"<b>{name}</b>",
#     #     'x': 1,  # מצמיד את הכותרת לימין
#     #     'xanchor': 'right',  # מוודא שהכותרת תתמקם בצד ימין
#     #     'font': {
#     #         'family': 'Arial',  # הפונט ברירת מחדל של Plotly
#     #         'color': '#7f7f7f',  # אפור כהה יותר כפי ש-Plotly משתמש
#     #         'size': 20  # אפשר לשנות את הגודל אם צריך
#     #     }
#     # },
#     # margin={'t': 100}  # Adds space at the top of the graph
#     # )

#     # הוספת מקרא מותאם אישית
#     legend_items = [
#         {'color': 'blue', 'label': f'{avg_national:.2f} :   ממוצע ארצי'},
#         {'color': 'orange', 'label': f'{avg_research} :ממוצע מחקרי'}
#     ]

#     #  מיקום התחלתי של המקרא
#     legend_x = 0.95
#     legend_y = 0.90
#     box_size = 0.02  # גודל הריבוע

#     for item in legend_items:
#         # הוספת ריבוע צבעוני
#         fig.add_shape(type="rect",
#                       x0=legend_x, x1=legend_x + box_size,
#                       y0=legend_y, y1=legend_y - box_size,
#                       line=dict(width=1, color='black'),
#                       fillcolor=item['color'],
#                       xref='paper', yref='paper')

#        # הוספת טקסט צמוד לריבוע
#         fig.add_annotation(x=legend_x - 0.01, y=legend_y - box_size / 2,
#                            text=item['label'], showarrow=False,
#                            font=dict(size=12, color="black"),
#                            xanchor='right', yanchor='middle',
#                            xref='paper', yref='paper')

#          # עדכון מיקום ה-y עבור הפריט הבא במקרא
#         legend_y -= box_size + 0.02

#     # הצגת הגרף
#     #fig.show()
#     return fig
    
# # draw_graph_gauge(4,3.5,4.0)
