import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State

df = pd.read_csv("StockData.csv")

months = df["Month"].unique()
companies = df["Company"].unique()
companyColors = {company: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, company in enumerate(companies)}

app = Dash(__name__, external_stylesheets=["/assets/style.css"])

app.layout = html.Div([
    html.H1("Stock Market Analysis Dashboard"),
    
    html.Div([
        html.Label("Select Month:", className="labels"),
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": month, "value": month} for month in months],
            value=months[0],
            className="dropdown"
        ),
        
        html.Label("Select Stock Price Metric:", className="labels"),
        dcc.RadioItems(
            id="radioButtons",
            options=[{"label": metric, "value": metric} for metric in ["Open", "Close", "High", "Low"]],
            value="Open",
            inline=True,
            className="radioButtons"
        ),
        
        html.Button("Update Charts", id="updateButton", className="button")
    ], className="options"),
    
    html.Div([
        dcc.Graph(id="barChart"),
        dcc.Graph(id="boxPlot")
    ], className="graphs")
])

@app.callback(
    [Output("barChart", "figure"), Output("boxPlot", "figure")],
    [Input("updateButton", "n_clicks")],
    [State("dropdown", "value"), State("radioButtons", "value")]
)
def updateGraphs(nClicks, selectedMonth, selectedMetric):
    filtered_df = df[df["Month"] == selectedMonth]
    
    barChart = px.bar(
        filtered_df.groupby("Company")[selectedMetric].mean().reset_index(),
        x="Company", y=selectedMetric, color="Company",
        color_discrete_map=companyColors,
        title=f"Average {selectedMetric} Price in {selectedMonth}"
    )
    
    boxPlot = px.box(
        filtered_df, x="Company", y=selectedMetric, color="Company",
        color_discrete_map=companyColors,
        title=f"Distribution of {selectedMetric} Prices in {selectedMonth}"
    )
    
    return barChart, boxPlot

if __name__ == "__main__":
    app.run(debug=True)

