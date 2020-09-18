import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import json

from urllib.request import urlopen

import matplotlib.pyplot as plt

import plotly.express as px

df = pd.read_excel('agg.xlsx')

with urlopen(
    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
) as response:
    counties = json.load(response)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
This is my first deployed app
'''

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

app.layout = html.Div([
	html.Div(className='row',
			 children=[
				html.Div(className='four columns div-user-controls',
						 children=[
							 html.H2('DASH - STOCK PRICES'),
							 html.P('Visualising time series with Plotly - Dash.'),
							 html.P('Pick one or more stocks from the dropdown below.'),
							 html.Div(
								 className='div-for-dropdown',
								 children=[
									 dcc.Dropdown(id='raceselector', options=get_options(df['race'].unique()),
												  multi=True, value=[df['stock'].sort_values()[0]],
												  style={'backgroundColor': '#1E1E1E'},
												  className='raceselector'
												  ),
								 ],
								 style={'color': '#1E1E1E'})
							]
						 )
			 ]
			)
	
	]
    #dcc.Markdown(children=top_markdown_text),
)

if __name__ == '__main__':
    app.run_server(debug=True)







