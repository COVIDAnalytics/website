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
df = df.loc[:,["Country","Median Age","Mortality"]]
df = df.dropna()

nav = Navbar()

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
                     html.H5('Select the Country'),
                     html.Div(dcc.Dropdown(
                         id = 'country_pop_dropdown',
                         options = [{'label': x, 'value': x} for x in set(df.Country.values)],
                         value = 'China'
                     )),
                     html.H5('Select Age Range'),
                     html.Div([
                         html.Div(dcc.Dropdown(
                             id = 'age1_pop_dropdown',
                             options = [{'label': x, 'value': x} for x in range(0,120)],
                             value = '20',
                             style={'width': '40%', 'display': 'inline-block'}
                             ),
                         ),
                         html.Div(dcc.Dropdown(
                             id = 'age2_pop_dropdown',
                             options = [{'label': x, 'value': x} for x in range(0,120)],
                             value = '90',
                             style={'width': '40%', 'display': 'inline-block'}),
                         ),
                     ]),
                     html.H5('Select Start and End Date'),
                     html.Div([
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=dt(2020, 1, 1),
                            max_date_allowed=dt(2020, 4, 1),
                            initial_visible_month=dt(2020, 1, 1),
                            end_date=dt(2020, 4, 1).date()
                        ),
                        html.Div(id='output-container-date-picker-range')
                    ]),
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

def build_graph(country):
    data = [go.Scatter(x = df.loc[df.Country == country]["Median Age"],
                            y = df.loc[df.Country == country]["Mortality"],
                            marker = {'color': 'orange'})]
    graph = dcc.Graph(
               figure = {
                   'data': data,
                   'layout': go.Layout(
                        title = '{} Median Age vs Mortality'.format(country),
                        yaxis = {'title': 'Mortality Percentage'},
                        hovermode = 'closest',
                        font={'color': '#FFFFFF'},
                        paper_bgcolor='gray',
                        plot_bgcolor='gray'
                        )
                    },
                 )
    return graph
