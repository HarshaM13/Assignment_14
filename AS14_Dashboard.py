import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib
import plotly
from dash import html, Dash
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

df = pd.read_csv("data/processed/df_covid_val_pred.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("COVID Deaths Dashboard", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="month",
        clearable=False,
        options=[{"label": m, "value": m} for m in df['month'].unique()],
        value=df['month'].unique()[0],
        style={"width": "50%", "margin": "auto"}
    ),

    html.Div([
        dcc.Graph(id='kpi_deaths'),  # ✅ Added KPI card
    ], style={"margin": "20px 0"}),

    html.Div([
        dcc.Graph(id='graph1'),
        dcc.Graph(id='graph2'),
        dcc.Graph(id='graph4')
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"})
])

@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('kpi_deaths', 'figure'),
     Output('graph4', 'figure')],
    Input('month', 'value')
)
def update_graphs(selected_month):
    filtered_df = df[df['month'] == selected_month]

    # Graph 1: Bar chart of Deaths by Date
    fig1 = px.bar(filtered_df, x="Date", y="Deaths", title=f"Deaths in {selected_month}", text="Deaths")
    fig1.update_traces(textposition="outside")

    # Graph 2: Bar chart of Predicted Deaths by Date
    fig2 = px.bar(filtered_df, x="Date", y="Predicted_Deaths", title=f"Predicted Deaths in {selected_month}", text="Predicted_Deaths")
    fig2.update_traces(textposition="outside")

    # KPI Card: Total Deaths
    total_deaths = filtered_df["Deaths"].sum()
    fig3 = go.Figure(go.Indicator(
        mode="number",
        value=total_deaths,
        title={"text": f"Total Deaths in {selected_month}"},
        number={"valueformat": ",", "font": {"size": 40}}
    ))
    fig3.update_layout(height=250, margin=dict(t=50, b=0, l=0, r=0))

    # Graph 4: Line chart for overall trend
    fig4 = px.line(df, x="Date", y=["Deaths", "Predicted_Deaths"], title="Overall Trend of Deaths and Predictions")

    return fig1, fig2, fig3, fig4

if __name__ == "__main__":
    app.run(port=8060, debug=True)
