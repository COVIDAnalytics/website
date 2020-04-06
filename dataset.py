### Data
import pandas as pd
import pickle
from datetime import datetime as dt
import urllib
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
from assets.mappings import data_cols

nav = Navbar()
footer = Footer()

dataset = "data/clinical_outcomes_database.csv"
ref_data = "data/reference_ranges.csv"

ref = pd.read_csv(ref_data)
df = pd.read_csv(dataset)

data_csv_string = df.to_csv(index=False, encoding='utf-8')
data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)
ref_data_csv_string = ref.to_csv(index=False, encoding='utf-8')
ref_data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(ref_data_csv_string)

df = df.loc[:,data_cols]
df = df.head(50)

table = dash_table.DataTable(
			id="data-table",
		    data=df.to_dict('records'),
		    columns=[{'id': c, 'name': c} for c in df.columns],
			style_data={
		        'whiteSpace': 'normal',
		        'height': 'auto',
		    },
			style_table={
				'overflowX': 'auto',
				'maxHeight': '400px',
				'overflowY': 'auto',
				'border': 'thin lightgrey solid',
			},
			style_cell={
		        'height': 'auto',
		        'minWidth': '0px',
				'width': '180px',
				'maxWidth': '180px',
		        'whiteSpace': 'normal',
				'textAlign': 'center',
				'font_size': '14px',
				'font-family': 'arial',
		    },
			style_data_conditional=[
		        {
		            'if': {'row_index': 'odd'},
		            'backgroundColor': 'rgb(248, 248, 248)'
		        }
		    ],
		    style_header={
		        'backgroundColor': 'rgb(230, 230, 230)',
		        'fontWeight': 'bold'
		    },
			fixed_rows={ 'headers': True, 'data': 0 },
		)

body = dbc.Container([
	dbc.Row(
        [
			dbc.Col([
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
    dbc.Row([
			dbc.Col(
				html.Div(
					html.A(
						"Download the Data",
						id="download-link",
						download=dataset,
						href=data_csv_string,
	        			target="_blank"
					),
					style={'text-align':"center"}
				)
			),
			dbc.Col(
				html.Div(
					html.A(
						"Download the Reference",
						id="download-reference-link",
						download=ref_data,
						href=ref_data_csv_string,
	        			target="_blank"
					),
					style={'text-align':"center"}
				)
			),
			]
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

],
className="page-body"
)

def Dataset():
    layout = html.Div([nav, body, footer],className="site")
    return layout
