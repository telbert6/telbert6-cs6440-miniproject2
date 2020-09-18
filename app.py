import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output


import pandas as pd
import json

from urllib.request import urlopen

import matplotlib.pyplot as plt

import plotly.express as px

df = pd.read_csv("agg.csv")

with open("counties.json") as json_file:
    counties = json.load(json_file)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = """
This is my first deployed app
"""


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({"label": i, "value": i})

    return dict_list


app.layout = html.Div(
    [
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("DASH - STOCK PRICES"),
                        html.P("Visualising time series with Plotly - Dash."),
                        html.P("Pick one or more stocks from the dropdown below."),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="raceselector",
                                    options=get_options(df["Race"].unique()),
                                    multi=True,
                                    value=[df["Race"].sort_values()[0]],
                                    style={"backgroundColor": "#1E1E1E"},
                                    className="raceselector",
                                ),
                            ],
                            style={"color": "#1E1E1E"},
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            className="eight columns div-for-charts bg-grey",
            children=[
                dcc.Graph(id="usmap", config={"displayModeBar": False}, animate=True)
            ],
        ),
    ]
    # dcc.Markdown(children=top_markdown_text),
)


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({"label": i, "value": i})

    return dict_list


app.layout = html.Div(
    [
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("DASH - STOCK PRICES"),
                        html.P("Visualising time series with Plotly - Dash."),
                        html.P("Pick one or more stocks from the dropdown below."),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="raceselector",
                                    options=get_options(df["Race"].unique()),
                                    multi=True,
                                    value=[df["Race"].sort_values()[0]],
                                    style={"backgroundColor": "#1E1E1E"},
                                    className="raceselector",
                                ),
                            ],
                            style={"color": "#1E1E1E"},
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            className="eight columns div-for-charts bg-grey",
            children=[
                dcc.Graph(id="usmap", config={"displayModeBar": False}, animate=True)
            ],
        ),
    ]
    # dcc.Markdown(children=top_markdown_text),
)


# Callback for timeseries price
@app.callback(Output("usmap", "figure"), [Input("raceselector", "value")])
def update_race(selected_dropdown_value):
    field = "SP_DEPRESSN"
    
    trace1 = []

    plot_df = pd.DataFrame(
        df[df.Field == field]
        .groupby("fipscd")
        .agg({"Cases": sum, "Patients": sum})
    ).reset_index()

    plot_df["% of Patients"] = plot_df.Cases / plot_df.Patients

    fig = px.choropleth_mapbox(
        plot_df,
        geojson=counties,
        locations="fipscd",
        color="% of Patients",
        color_continuous_scale="Viridis",
        range_color=(0, plot_df["% of Patients"].max()),
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.5,
        labels={"% of Patients": "% of Patients"},
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)







