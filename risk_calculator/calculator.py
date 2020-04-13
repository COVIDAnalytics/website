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

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
              html.H2("Clinical Rick Calculator")
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                [
                    dcc.Markdown(
                         """Severe COVID-19 patients require our most limited health care resources,\
                          ventilators and intensive care beds. As a result, physicians have the hard \
                          responsibility to decide which patients should have priority access to these \
                          resources. To help them make an informed decision, we construct and publish \
                          patient risk calculators tailored for COVID-19 patients.
                         """,
                    ),
                    dcc.Markdown(
                         """ **Disclaimer:** A model is only as good as the data it is trained on. We will \
                         release new versions of the calculator as the amount of data we receive from \
                         our partner institutions increases. If you are a medical institution and are \
                         willing to contribute to our effort, feel free to reach out to us [here](/contact).
                         """,
                    ),
                    dcc.Markdown(
                         """ **Data** (as of 2020/04/10): Our model is trained on 496 patients from the Azienda \
                         Socio-Sanitaria Territoriale di Cremona [ASST Cremona](https://www.asst-cremona.it/) which includes the Ospedale \
                         di Cremona, Ospedale Oglio Po and other minor public hospitals in the Province of \
                         Cremona. Cremona is one of the most hit italian provinces in Lombardy in the Italian \
                         COVID-19 crisis with a total of several thousand positive cases to date. Given our training \
                         population, we are most confident about the relevance of our model to: (a) Western population; \
                         (b) Severe to acute patients; (c) Congested hospitals. \
                         """,
                    ),
                    dcc.Markdown(
                         """ **This is a developmental version. It is not intended for patient or clinician use.\
                          It is available only to solicit input about its future development.**
                         """,
                         ),
                ]
                )
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
                html.H5('Insert the features below into the risk calculator.')
            ),
        ]),
        dbc.Row(build_feature_cards()),
        dbc.Row(dbc.Col(dbc.Button("Submit", color="primary",id="submit-features-calc"))),
    ],
    className="page-body"
)

def RickCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout
