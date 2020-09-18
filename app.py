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

    for stock in selected_dropdown_value:
        trace1.append(
            go.Choroplethmapbox(
                geojson=counties,
                locations=plot_df["fipscd"],
                z=plot_df["% of Patients"],
                colorscale="Viridis",
                zmin=0,
                zmax=12,
                marker_opacity=0.5,
                marker_line_width=0,
            )
        )
		

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {
        "data": data,
        "layout": go.Layout(
            colorway=["#5E0DAC", "#FF4F00", "#375CB1", "#FF7400", "#FFF400", "#FF0056"],
            template="plotly_dark",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            margin={"b": 15},
            hovermode="x",
            autosize=True,
            title={"text": "Stock Prices", "font": {"color": "white"}, "x": 0.5}#,
            #xaxis={"range": [df_sub.index.min(), df_sub.index.max()]},
        ),
    }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)







