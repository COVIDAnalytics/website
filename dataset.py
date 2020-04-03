### Data
import pandas as pd
import pickle
from datetime import datetime as dt
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import flask
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from navbar import Navbar
from footer import Footer
from interactive import demographics

dataset = 'data/covid_analytics.csv'
df = pd.read_csv(dataset)

nav = Navbar()
footer = Footer()

table = dbc.Table.from_dataframe(
			df,
			id="data-table",
			striped=True,
			bordered=True,
			hover=True,
			responsive=True,
		)


body = dbc.Container([
	dbc.Row(
        [
			dbc.Col([
				html.H1("COVID-19 Analytics"),
            	html.H2("Dataset"),
                html.P('In the fog of war of the Covid-19 pandemic, a critical factor inhibiting \
				 effective decision making at regional, national, and global levels is a lack of \
				 relevant data on patient outcomes. We hope to partially alleviate this problem by\
				 sharing the following dataset, which aggregates data from over 100 published \
				 clinical studies and preprints released between December 2019 and March 2020. '),
				html.P('We would like to remind the reader that the raw data in this dataset should not \
				 be used to estimate trends in the general population such as mortality rates. \
				 Indeed, this dataset is largely derived from studies run in hospitals and nations\
				 affected with SARS-COV-2 generally only admit seriously affected patients to \
				 hospitals. However, it should be possible to derive reasonably accurate estimates\
				 of these quantities by (a) accounting for the prevalence of asymptomatic \
				 patients, and (b) only including sufficiently representative studies. '),
				html.P('At a high level, each row of the dataset represents a cohort of patients.\
				 Some papers study a single cohort, while others study several cohorts, \
				 and still others report results about one cohort and one or more subcohorts;\
				 all of these are included as rows in the dataset. '
				 )
				 ])
		 ]
	 ),
    dbc.Row(
			dbc.Col(
				html.Div(
					html.A(
						"Download the Dataset",
						id="download-link",
						download=dataset,
						href="",
	        			target="_blank"
					),
					 style={'text-align':"center"}
				)
			)
	),
  dbc.Row(
           [
              dbc.Col(
                [
                   dbc.Col([table,]) ,
                ],
				width=12
             ),
            ],
        ),

])

def Dataset():
    layout = html.Div([nav, body, footer])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Dataset()
app.title = "MIT_ORC_COVID19"
