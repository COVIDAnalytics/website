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
from projections import build_us_map
from assets.colMapping import states

nav = Navbar()

def build_tom_us_map():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return build_us_map(tomorrow)

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                html.H1("COVID-19 Analytics"),
                html.H2("Predictive Tools"),
                html.P(
                     """\
                     MIT’s Operations Research Center provides open source interactive tools and dataset to predict patients outcome probabilities, including their potential Intensive Care Unit needs and expected length of stay in hospital.

                     We aim to rapidly develop, vet, and deliver tools for use by hospitals in the United States to combat the spread of COVID-19.

                     """
                )
            ],
            width=3.5
            ),
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
    className="hompage-body",
)

def Homepage():
    layout = html.Div([nav, body])
    return layout
