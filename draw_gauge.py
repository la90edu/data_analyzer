import plotly.graph_objects as go
import streamlit as st 

def draw_graph_gauge(name,value,avg_national,avg_research):
# נתונים
# value = 3.7  
# avg_national = 3.5  
# avg_research = 4.0  

 
# יצירת גרף
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"<b>{name}</b>", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [1, 5]},
            'steps': [
                {'range': [avg_national - 0.05, avg_national + 0.05], 'color': "blue"},
                {'range': [avg_research - 0.05, avg_research + 0.05], 'color': "orange"}
            ],
            'bar': {'color': "green", 'thickness': 0.3}
        }
    ))
    
    # # הוספת margin ב-layout
    # fig.update_layout(
    # title={
    #     'text': f"<b>{name}</b>",
    #     'x': 1,  # מצמיד את הכותרת לימין
    #     'xanchor': 'right',  # מוודא שהכותרת תתמקם בצד ימין
    #     'font': {
    #         'family': 'Arial',  # הפונט ברירת מחדל של Plotly
    #         'color': '#7f7f7f',  # אפור כהה יותר כפי ש-Plotly משתמש
    #         'size': 20  # אפשר לשנות את הגודל אם צריך
    #     }
    # },
    # margin={'t': 100}  # Adds space at the top of the graph
    # )

    # הוספת מקרא מותאם אישית
    legend_items = [
        {'color': 'blue', 'label': f'{avg_national:.2f} :   ממוצע ארצי'},
        {'color': 'orange', 'label': f'{avg_research} :ממוצע מחקרי'}
    ]

    #  מיקום התחלתי של המקרא
    legend_x = 0.95
    legend_y = 0.90
    box_size = 0.02  # גודל הריבוע

    for item in legend_items:
        # הוספת ריבוע צבעוני
        fig.add_shape(type="rect",
                      x0=legend_x, x1=legend_x + box_size,
                      y0=legend_y, y1=legend_y - box_size,
                      line=dict(width=1, color='black'),
                      fillcolor=item['color'],
                      xref='paper', yref='paper')

       # הוספת טקסט צמוד לריבוע
        fig.add_annotation(x=legend_x - 0.01, y=legend_y - box_size / 2,
                           text=item['label'], showarrow=False,
                           font=dict(size=12, color="black"),
                           xanchor='right', yanchor='middle',
                           xref='paper', yref='paper')

         # עדכון מיקום ה-y עבור הפריט הבא במקרא
        legend_y -= box_size + 0.02

    # הצגת הגרף
    #fig.show()
    return fig
    
# draw_graph_gauge(4,3.5,4.0)    
