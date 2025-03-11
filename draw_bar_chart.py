import plotly.express as px
import pandas
df = px.data.iris()
 
fig = px.bar(df, x="sepal_width", y="sepal_length", color="species")
fig.show()