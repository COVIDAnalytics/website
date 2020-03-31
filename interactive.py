### Data
import pandas as pd
import pickle
from datetime import datetime as dt
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar

df = pd.read_csv('data/0327.csv')

nav = Navbar()

categories = ["Comorbidities","Symptoms","Treatment"]
all_options = {
    'Comorbidities': ["Current Smoker"
                          ,"Any Comorbidity"
                          ,"Hypertension"
                          ,"Diabetes"
                          ,"Coronary.heart.disease"
                          ,"Chronic.obstructive.lung"
                          ,"Cancer..Any."
                          ,"Chronic.kidney.renal.disease"
                          ,"Other"
                     ],
    'Symptoms': ["Fever,temperature > 37.3 C"
                 ,"Average temperature (C)"
                 ,"Cough"
                 ,"Shortness of Breath (Dyspnoea)"
                 ,"Headache"
                 ,"Sputum"
                 ,"Muscle.Pain (Myalgia)"
                 ,"Fatigue"
                 ,"Diarrhoea"
                 ,"Nausea/Vomiting"
                 ,"Loss of Appetite"
                 ,"Sore Throat/Stuffy Nose"
                ],
    'Treatment': ["Antibiotic",
                "Antiviral",
                "Corticosteroid",
                "Intravenous Immunoglobin",
                "Nasal Cannula",
                "High flow nasal cannula oxygen therapy",
                "Noninvasive mechanical ventilation",
                "Invasive mechanical ventilation",
                "ECMO",
                "Glucocorticoid",
                "Renal replacement therapy"],
}

demographics = ["Median Age", "Gender"]

body = dbc.Container(
    [
        dbc.Row(
          [
            dbc.Col(
              [
              html.H1("COVID-19"),
              html.H2("Interactive Graphs")
              ]
            ),
          ],
          ),
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H5('What would you like to compare?'),
                     html.Div(dcc.Dropdown(
                         id = 'categories_dropdown',
                         options = [{'label': x, 'value': x} for x in categories],
                         value = 'Comorbidities',
                         style={'width': '80%', 'display' : 'inline-block'}),
                     ),
                     html.Div(
                        id='display-selected-values',
                        style={'width': '100%', 'display': 'inline-block','color': 'white'}),
                     html.Div([
                         html.Div(dcc.Dropdown(
                             id = 'y_axis_dropdown',
                             value = 'Current Smoker',
                             style={'width': '80%', 'display': 'inline-block'}
                             ),
                         )
                     ]),
                     html.H6('Select the Demographic (Horizontal Axis)'),
                     html.Div(dcc.Dropdown(
                         id = 'x_axis_dropdown',
                         options = [{'label': x, 'value': x} for x in demographics],
                         value = 'Gender',
                         style={'width': '80%', 'display' : 'inline-block'}),
                     ),
                   ],
                  md=4,
               ),
              dbc.Col(
                [
                    html.Div(
                    id = 'interactive_graph',
                    children = [],
                    style={
                        'width': '100%',
                        'display': 'inline-block',
                        }
                    ),
                ]
             ),
            ],
        ),
   ],
className="mt-4",
)

def App():
    layout = html.Div(
    [
        nav,
        body
    ])
    return layout


def build_graph(y_title,x_title):
    global df
    cols = [x_title,y_title] + ["PopSize","Survivors"]
    if y_title not in df.columns or x_title not in df.columns:
        return None
    df = df[cols]
    df = df.dropna()

    data = [
    #TODO: DO and outer for for 3 ranges of population, each time changing size of point
        go.Scatter(
            x=df[df['Survivors'] == i][x_title],
            y=df[df['Survivors'] == i][y_title],
            text=df[df['Survivors'] == i]['Survivors'],
            mode='markers',
            opacity=0.8,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'black'}
            },
            name=i
        ) for i in df.Survivors.unique()
    ]

    graph2 = dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': data,
            'layout': go.Layout(
                xaxis={'title': x_title},
                yaxis={'title': y_title},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
    return graph2
