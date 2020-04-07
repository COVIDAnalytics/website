### Data
import pandas as pd
import datetime
import urllib
### Graphing
import plotly.graph_objects as go
import plotly.express as px
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer
from assets.mappings import states, colors

nav = Navbar()
footer = Footer()

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                html.H2("Projections"),
                html.P("""\
                        This page presents the predictions of a new epidemiological model for COVID-19 infections, hospitalizations, and deaths in all states of the United States. The model is based on the widely successful SEIR (Susceptible-Exposed-Infected-Recovered) model.
                       """),
                dcc.Markdown('''You can read more about the model [here](/projections_documentation).'''),
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Date:',id="date-projections"),
                html.Div(
                    dcc.DatePickerSingle(
                        id='us-map-date-picker-range',
                        min_date_allowed=min(df_projections.Day.values),
                        max_date_allowed=max(df_projections.Day.values),
                        date=oneWeekFromNow,
                        initial_visible_month=oneWeekFromNow,
                        style={'margin-bottom':20}
                    ),
                    id="date-projections-picker-div"
                ),
            ],
            ),
        ]
        ),
        dbc.Row(
        [
            html.Div(
                id='us-stats-title',
                style={
                    'width': '100%',
                    'color': 'black',
                    'text-align': 'center',
                    'font-size': 30,
                    'font-weight':'bold'
                    }
            ),
        ],
        ),
        dbc.CardDeck(
        [
            dbc.Card([], id = 'us_tot_det', color="dark", inverse=True, style={'margin-bottom':20,'padding-top':20}),
            dbc.Card([], id = 'us_tot_death', color="dark", inverse=True, style={'margin-bottom':20,'padding-top':20}),
            dbc.Card([], id = 'us_active', color="dark", inverse=True, style={'margin-bottom':20,'padding-top':20}),
            dbc.Card([], id = 'us_active_hosp', color="dark", inverse=True, style={'margin-bottom':20,'padding-top':20}),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Predicted Value:',id="date-projections"),
                    html.Div(
                        dcc.Dropdown(
                            id = 'us_map_dropdown',
                            options = [{'label': x, 'value': x} for x in cols],
                            value = 'Active',
                        ),
                    ),
            ],
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                    id = 'us_map_projections',
                    children = [],
                ),
            ]
            )
        ],
        ),
        dbc.Row(
        [
            html.P('* Gray states correspond to no projection as their number \
                    of confirmed cases so far is too low for a reliable estimation.\
                    We will update on a daily basis.',
                    style={'color':'gray'}
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('State:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'state_dropdown',
                        options = [{'label': x, 'value': x} for x in df_projections.State.unique()],
                        value = 'US',
                    )
               )
            ],
            ),
        ],
        ),
         dbc.Row(
         [
               dbc.Col(
               [
                     html.Div(
                         id = 'state_projection_graph',
                         children = [],
                         style={
                             'width': '100%',
                             'display': 'inline-block',
                             }
                     ),
                ]
                )
          ],
          ),
         dbc.Row([
            dbc.Col(
                html.Div(
                    html.A(
                        "Download the Data",
                        id="download-link",
                        download="covid_analytics_projections.csv",
                        href=data_csv_string,
                        target="_blank"
                    ),
                    style={'text-align':"center"}
                )
            ),
            ]
        ),
   ],
   className="page-body"
)

def VentilatorAllocations():
    layout = html.Div([nav, body, footer],className="site")
    return layout
