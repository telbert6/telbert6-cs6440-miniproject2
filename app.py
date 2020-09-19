import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import sys

import pandas as pd
import json

from urllib.request import urlopen

import matplotlib.pyplot as plt

import plotly.express as px

df = pd.read_csv("agg.csv", dtype={'fipscd': str})

with open("counties.json") as json_file:
	counties = json.load(json_file)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = """
This is my first deployed app
"""

def state_center_zoom(state, df):
	state_code = list(df[df.State == state]['fipscd'])[0][:2]
	#print(f"code: {state_code}", file=sys.stderr)
	
	coords = list(pd.DataFrame([
		list(pd.DataFrame(county['geometry']['coordinates'][0]).mean(axis = 0))
		for county in counties['features']
		if county['properties']['STATE'] == state_code
	]).mean(axis = 0))
	
	print(f"coords: {coords}", file=sys.stderr)
	
	return coords, 4

def get_options(list_stocks):
	dict_list = []
	for i in list_stocks:
		dict_list.append({"label": i, "value": i})

	return dict_list

def get_options(list_stocks, add_all = False, add_all_label = "All"):
	
	if add_all:
		dict_list= [{
			"label":add_all_label,
			"value":"All"
		}]
	else:
		dict_list = []
	
	
	for i in list_stocks:
		dict_list.append({"label": i, "value": i})

	

	return dict_list


app.layout = html.Div(
	[
		html.Div(
			className="row",
			children=[
				html.H2("Chronic Conditions Among Patients in 2008-2009"),
				html.Div(
					className="twelve columns div-user-controls",
					children=[
						html.Div(
							className="div-for-dropdown",
							children=[
								html.Div([
									html.P('Race:'),
									dcc.Dropdown(
										id="raceselector",
										options=get_options(df["Race"].unique()),
										multi=True,
										value=list(df["Race"].unique()),
										#style={"backgroundColor": "#1E1E1E"},
									)
								], className="three columns div-user-controls"),
								html.Div([
									html.P('Sex:'),
									dcc.Dropdown(
										id="sexselector",
										options=get_options(
											df["Sex"].unique(),
											add_all = True, 
											add_all_label = "Both"),
										multi=False,
										value="All"
									)
								], className="three columns div-user-controls"),
								html.Div([
									html.P('State:'),
									dcc.Dropdown(
										id="stateselector",
										options=get_options(
											df["State"].unique(),
											add_all = True, 
											add_all_label = "All"),
										multi=False,
										value="All"
									)
								], className="three columns div-user-controls"),
								html.Div([
									html.P('Condition:'),
									dcc.Dropdown(
										id="conditionselector",
										options=get_options(df["Field"].unique()),
										multi=False,
										value="All"
									)
								], className="three columns div-user-controls")
							]
						),
					],
				)
			],
		),
		html.Div(
			[
				dcc.Graph(
					id="usmap", 
					config={"displayModeBar": False}
				),
				html.Div(
					[
						dcc.Graph(
							id="sex_patient_pie", 
							config={"displayModeBar": False},
							className="four columns div-for-charts bg-grey"
						),
						dcc.Graph(
							id="sex_case_pie", 
							config={"displayModeBar": False},
							className="four columns div-for-charts bg-grey"
						),
						dcc.Graph(
							id="sex_expense_pie", 
							config={"displayModeBar": False},
							className="four columns div-for-charts bg-grey"
						)
					],
					className="twelve columns div-for-charts bg-grey"
				),
				html.Div(
					[
						dcc.Graph(
							id="race_patient_pie", 
							config={"displayModeBar": False}
							,
							className="four columns div-for-charts bg-grey"
						),
						dcc.Graph(
							id="race_case_pie", 
							config={"displayModeBar": False}
							,
							className="four columns div-for-charts bg-grey"
						),
						dcc.Graph(
							id="race_expense_pie", 
							config={"displayModeBar": False}
							,
							className="four columns div-for-charts bg-grey"
						),
						
					],
					className="twelve columns div-for-charts bg-grey"
				)
			],
			className="twelve columns div-for-charts bg-grey"
		),
	]
	# dcc.Markdown(children=top_markdown_text),
)

# Callback for timeseries price
@app.callback(
	
	Output("usmap", "figure"), 
	Output("race_patient_pie", "figure"),
	Output("race_case_pie", "figure"),
	Output("race_expense_pie", "figure"),
	Output("sex_patient_pie", "figure"),
	Output("sex_case_pie", "figure"),
	Output("sex_expense_pie", "figure"),
	[
		Input("raceselector", "value"), 
		Input("sexselector", "value"),
		Input("stateselector", "value"),
		Input("conditionselector", "value")
	]
)
def update_map(race_values, sex_value, state_value, condition_value):
	#all_race = "All" in race_values
	all_sex = "All" == sex_value
	all_states = "All" == state_value
	
	if len(race_values) == 0:
		race_values = ["White", "Black", "Hispanic", "Other"]
	
	#print(f"All filters: {all_race}, {all_sex}", file=sys.stderr)

	trace1 = []


	filtered_df = df[
			df.Field.apply(lambda condition: condition == condition_value)
			& df.Race.apply(lambda race: race in race_values)
			& df.Sex.apply(lambda sex: all_sex or sex == sex_value)
			& df.State.apply(lambda state: all_states or state == state_value)
			& (df.Patients >= 5)
		]

	map_plot_df = pd.DataFrame(
		filtered_df
		.groupby(["fipscd", "State", "County"])
		.agg({"Cases": sum, "Patients": lambda x: sum(x)})
	).reset_index()
	map_plot_df["% of Patients"] = round(map_plot_df.Cases / map_plot_df.Patients * 100, 1)
	
	
	fig_map = px.choropleth_mapbox(
		map_plot_df,
		geojson=counties,
		locations="fipscd",
		color="% of Patients",
		color_continuous_scale="Viridis",
		range_color=(0, map_plot_df["% of Patients"].max()),
		mapbox_style="carto-positron",
		zoom=3,
		center={"lat": 37.0902, "lon": -95.7129},
		opacity=0.5,
		labels={"% of Patients": "% of Patients"},
		hover_name = map_plot_df.apply(lambda x: f"{x['County']}, {x['State']}", axis = 1),
		hover_data = ['Cases', 'Patients']
	)
	fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
	
	#pie charts
	race_pie_plot_df = pd.DataFrame(
		filtered_df
		.groupby(["Race"])
		.agg({"Cases": sum, "Patients": sum, "Total Expense":sum})
	)
	
	race_pie_plot_df = race_pie_plot_df.loc[
		[
			race
			for race in ["White", "Black", "Hispanic", "Other"]
			if race in list(race_pie_plot_df.index)
		]
	].reset_index()
	race_pie_plot_df['Average Expense Per Case'] = round(race_pie_plot_df['Total Expense'] / race_pie_plot_df['Cases'], 2)
	race_patient_pie_fig = go.Figure(
		data = [
			go.Pie( 
				#race_pie_plot_df, 
				values=race_pie_plot_df['Patients'], 
				labels=race_pie_plot_df['Race'], 
				title='Total Patients by Race',
				sort=False
			)
		]
	)
	race_case_pie_fig = go.Figure(
		data = [
			go.Pie(
				#race_pie_plot_df, 
				values=race_pie_plot_df['Cases'], 
				labels=race_pie_plot_df['Race'],
				title='Cases by Race',
				sort=False
			)
		]
	)
	race_expense_pie_fig = go.Figure(
		data = [
			go.Pie(
				#race_pie_plot_df,  
				values=race_pie_plot_df['Average Expense Per Case'], 
				labels=race_pie_plot_df['Race'],
				title='Average Expense per Visit',
				sort=False
			)
		]
	)
	
	
	
	sex_pie_plot_df = pd.DataFrame(
		filtered_df
		.groupby(["Sex"])
		.agg({"Cases": sum, "Patients": sum, "Total Expense":sum})
	)
	sex_pie_plot_df = sex_pie_plot_df.loc[
		[
			sex
			for sex in ["Female", "Male"]
			if sex in list(sex_pie_plot_df.index)
		]
	].reset_index()
	sex_pie_plot_df['Average Expense Per Case'] = round(sex_pie_plot_df['Total Expense'] / sex_pie_plot_df['Cases'], 2)
	sex_patient_pie_fig = go.Figure(
		data = [
			go.Pie(
				#sex_pie_plot_df, 
				values=sex_pie_plot_df['Patients'], 
				labels=sex_pie_plot_df['Sex'],
				title='Total Patients by Sex',
				sort=False
			)
		]
	)
	sex_case_pie_fig = go.Figure(
		data = [
			go.Pie(
				#sex_pie_plot_df, 
				values=sex_pie_plot_df['Cases'], 
				labels=sex_pie_plot_df['Sex'],
				title='Cases by Sex',
				sort=False
			)
		]
	)
	sex_expense_pie_fig = go.Figure(
		data = [
			go.Pie(
				#sex_pie_plot_df, 
				values=sex_pie_plot_df['Average Expense Per Case'], 
				labels=sex_pie_plot_df['Sex'], 
				title='Average Expense',
				sort=False
			)
		]
	)
	
	
	return fig_map, race_patient_pie_fig, race_case_pie_fig, race_expense_pie_fig, sex_patient_pie_fig, sex_case_pie_fig, sex_expense_pie_fig


if __name__ == '__main__':
	app.run_server(debug=True)