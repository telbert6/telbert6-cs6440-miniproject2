import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import json
import os
import pprint

from urllib.request import urlopen

import matplotlib.pyplot as plt

import plotly.express as px

import dash
import dash_html_components as html


#df = pd.read_exel('agg.xlsx')

#with urlopen(
#    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
#) as response:
#    counties = json.load(response)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
This is my first deployed app
'''

app.layout = html.Div([

    dcc.Markdown(children=top_markdown_text),

])

if __name__ == '__main__':
    app.run_server(debug=True)







