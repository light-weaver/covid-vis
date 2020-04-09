import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd

import plotly.graph_objects as go
import numpy as np

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
data_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
data = pd.read_csv(data_url)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="COVID-19 Dashboard"),
        dcc.Dropdown(id="coloraxes"),
        dcc.Graph(
            id="chloropleth",
            figure=go.Figure(go.Choropleth(locationmode="country names")),
        ),
        dcc.Slider(
            id="Date",
            min=0,
            max=len(data["Date"].unique()) - 1,
            value=0,
            marks={
                i: {"label": str(date), "style": {"transform": "rotate(45deg)"}}
                for i, date in enumerate(data["Date"].unique())
            },
            step=None,
        ),
    ]
)


@app.callback(
    Output("chloropleth", "figure"), [Input("Date", "value")], [State("Date", "marks")]
)
def color_graph(date_val, dates):
    if date_val is None:
        PreventUpdate()
    date = dates[str(date_val)]["label"]
    fig = go.Figure()
    fig.add_choropleth(z=data[data["Date"]==date]["Confirmed"],
                   locations=data[data["Date"]==date]["Country"],
                   locationmode="country names"
                    )
    return(fig)


if __name__ == "__main__":
    app.run_server()
