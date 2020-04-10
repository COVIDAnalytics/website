### Data
import datetime
import pandas as pd

### Graphing
import plotly.graph_objects as go
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from projections.projections import build_us_map
from assets.mappings import states

nav = Navbar()
footer = Footer()

def build_tom_us_map():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return build_us_map(tomorrow)

data_card = dbc.Card(
    [
        dbc.CardImg(src="assets/images/data-1.jpg", top=True),
        dbc.CardBody(
            [
                html.H4("Data", className="card-title"),
                dcc.Markdown('''
                       130+ international Covid-19 clinical studies,
                       aggregated into a single [dataset](/dataset).
                       ''',
                ),
            ]
        ),
    ],
    style={"borderColor": "#900C3F"},
    className="h-100",
)

insights_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Insights", className="card-title"),
                dcc.Markdown('''
                      Key characteristics of COVID-19 patients in an
                      [interactive summary](/interactive-graph).
                  ''',
                ),
            ]
        ),
        dbc.CardImg(src="assets/images/insights-4.png", top=False),
    ],
    style={"borderColor": "#900C3F"},
    className="h-100"
)

projections_card = dbc.Card(
    [
        dbc.CardImg(src="assets/images/forecast-1.png", top=True),
        dbc.CardBody(
            [
                html.H4("Projections", className="card-title"),
                dcc.Markdown('''
                    State-by-state [predictions](/projections) of COVID-19 infections, hospital stays, and deaths.
                       ''',
                ),
            ]
        ),
    ],
    style={"borderColor": "#900C3F"},
    className="h-100"
)

ventilator_card = dbc.Card(
    [
        dbc.CardImg(src="assets/images/allocation-2.png", top=True),
        dbc.CardBody(
            [
                html.H4("Ventilator allocation", className="card-title"),
                dcc.Markdown('''
                       Leveraging delays between state peaks to [optimally re-use ventilators](/ventilator_allocation).'''
                ),
            ],
        ),
    ],
    style={"borderColor": "#900C3F"},
    className="h-100"
)

calculator_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Risk calculator", className="card-title"),
                dcc.Markdown('''
                      (Coming 4/12). Personalized calculator predicting ICU length of stay and mortality.''',
                ),
            ]
        ),
        dbc.CardImg(src="assets/images/tree-2.png", top=True),
    ],
    style={"borderColor": "#900C3F"},
    className="h-100"
)

body = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Markdown(
                     '''
                     We are a group of researchers from the [MIT](http://mit.edu/) [Operations Research Center](https://orc.mit.edu/), \
                     led by Professor [Dimitris Bertsimas](https://www.mit.edu/~dbertsim/). \
                     We aim to quickly develop and deliver tools for hospitals and policymakers in the US to combat the spread of COVID-19. \
                     This work represents a collaborative effort with [Hartford HealthCare](https://hartfordhealthcare.org/) \
                     and [ASST Cremona](https://www.asst-cremona.it) which have been providing us with data and support through the model creation process.
                     '''
                ),
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    data_card,
                    style={"margin": "0.5rem"},
                    xs=12,
                    sm=5,
                    md=5,
                    lg=2,
                ),
                dbc.Col(
                    insights_card,
                    style={"margin": "0.5rem"},
                    xs=12,
                    sm=5,
                    md=5,
                    lg=2,
                ),
                dbc.Col(
                    projections_card,
                    style={"margin": "0.5rem"},
                    xs=12,
                    sm=5,
                    md=5,
                    lg=2,
                ),
                dbc.Col(
                    ventilator_card,
                    style={"margin": "0.5rem"},
                    xs=12,
                    sm=5,
                    md=5,
                    lg=2,
                ),
                dbc.Col(
                    calculator_card,
                    style={"margin": "0.5rem"},
                    xs=12,
                    sm=5,
                    md=5,
                    lg=2,
                ),
            ],
            justify="around",
            no_gutters=True,
        ),
        dbc.Row(
        [
            dbc.Col(
            [
              html.Div(
                  id = 'us_map_homepage',
                  children = build_tom_us_map(),
              ),
            ]
            )
        ],
        )
    ],
    className="page-body"
)

def Homepage():
    layout = html.Div([nav, body, footer], className="site")
    return layout
