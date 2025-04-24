import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import os

# Load equity curve CSV
try:
    df = pd.read_csv("logs/equity_curve.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["timestamp", "NetLiq", "BuyingPower"])

# Convert timestamp if needed
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Judas Equity Curve"

app.layout = html.Div([
    html.H1("📈 Judas Sacred System – Equity Curve", style={"textAlign": "center"}),

    dcc.Graph(
        id="equity-curve-chart",
        figure={
            "data": [
                go.Scatter(x=df["timestamp"], y=df["NetLiq"], mode="lines+markers", name="NetLiq"),
                go.Scatter(x=df["timestamp"], y=df["BuyingPower"], mode="lines", name="Buying Power")
            ],
            "layout": go.Layout(
                xaxis={"title": "Time"},
                yaxis={"title": "Value (USD)"},
                legend={"x": 0, "y": 1},
                margin={"l": 40, "r": 20, "t": 40, "b": 40},
                hovermode="closest"
            )
        },
        style={"height": "70vh"}
    ),

    html.Div("Mobile-Optimized · Refresh chart by reloading page", style={"textAlign": "center", "marginTop": "20px", "fontSize": "14px"})
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)