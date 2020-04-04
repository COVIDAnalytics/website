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
from projections import build_us_map
from assets.mappings import states

nav = Navbar()
footer = Footer()

def build_tom_us_map():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return build_us_map(tomorrow)

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                dcc.Markdown(
                     '''
                     This website represents the effort of a group of about 20 graduate \
                     students in the [Operations Research Center](https://orc.mit.edu/) at [MIT](http://mit.edu/) under the guidance \
                     of [Professor Bertsimas](https://www.mit.edu/~dbertsim/). Our overarching objective is to rapidly develop, \
                     and deliver tools for use by hospitals, government officials, \
                     and healthcare institutions in the United States to combat the spread of COVID-19.
                     '''
                ),
                html.H5("In our website you will find the following:"),
                dcc.Markdown('''
                  1. [Data](/dataset) from over 130 scientific papers published in March 2020 \
                  about COVID-19 incidents in hospitals around the world. These data were curated and verified by the team.
                  2. [Descriptive analytics](/interactive-graph) from these papers that provide insights on a \
                  variety of aspects related to COVID-19 patients.
                  3. [Predictions](/projections) of COVID-19 infections, hospitalizations, and deaths in \
                  all states of the United States. It is based on a new epidemiological \
                  model that was specifically built for COVID-19.
                  4. We are in the process of developing a personalized prediction calculator \
                  that assesses the probability of length of stay at the ICU and mortality risk \
                  using the aggregate data the group has curated as well patients level data we \
                  received from major hospitals in Boston, US, Wuhan, China and Cremona, Italy. \
                  We expect this calculator to be released by Friday, April, 10. 2020.
                  5. Because the peak of the infection for different states occurs at different \
                  times, we have also developed an optimization model based on the epidemiological \
                  model that shows how different states can send ventilators to materially \
                  decrease the deficit over time. This idea can also be used at different hospitals \
                  within the same state.
                ''')
            ],
            ),
        ]
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
    layout = html.Div([nav, body, footer])
    return layout
