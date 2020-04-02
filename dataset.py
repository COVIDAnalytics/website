### Data
import pandas as pd
import pickle
from datetime import datetime as dt
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar

df = pd.read_csv('data/0332.csv')

categories = ["Comorbidities","Symptoms","Treatment"]
all_options = {
    'Comorbidities': ["Current smoker"
                          ,"Any Comorbidity"
                          ,"Hypertension"
                          ,"Diabetes"
                          ,"Coronary heart disease"
                          ,"Chronic obstructive lung"
                          ,"Cancer"
                          ,"Chronic kidney/renal disease"
                          ,"Other"
                     ],
    'Symptoms': ["Fever,temperature > 37.3 C"
                 ,"Average temperature (C)"
                 ,"Cough"
                 ,"Shortness of breath (dyspnoea)"
                 ,"Headache"
                 ,"Sputum"
                 ,"Muscle pain (Myalgia)"
                 ,"Fatigue"
                 ,"Diarrhoea"
                 ,"Nausea or vomiting"
                 ,"Loss of Appetite"
                 ,"Sore Throat/Stuffy Nose"
                ],
    'Treatment': ["Antibiotic",
                "Antiviral",
                "Corticosteroid",
                "Intravenous immunoglobin",
                "Nasal Cannula",
                "High-flow nasal cannula oxygen therapy",
                "Noninvasive mechanical ventilation",
                "Invasive mechanical ventilation",
                "ECMO",
                "Glucocorticoid",
                "Renal replacement therapy"],
}

demographics = ["Median Age", "Male Percentage"]

nav = Navbar()

table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True,)


body = dbc.Container([
	dbc.Row(
        [dbc.Col([html.H1("COVID-19"),
            	  html.H2("Dataset"),]),],),
	dbc.Row(
           [
               dbc.Col(
                  [ dbc.Row( html.H6('In the fog of war of the Covid-19 pandemic, a critical factor inhibiting effective decision making at regional, national, and global levels is a lack of relevant data on patient outcomes. We hope to partially alleviate this problem by sharing the following dataset, which aggregates data from over 100 published clinical studies and preprints released between December 2019 and March 2020.'),),
                  ],md=4
               ),
              dbc.Col(
                [
                   dbc.Col([table,]) ,
                ],md=8
             ),
            ],
        ),
	
])

            
def Dataset():
    layout = html.Div([
                    nav,
                    body
                    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Dataset()
app.title = "MIT_ORC_COVID19"