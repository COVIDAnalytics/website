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
                         """\
                            blah
                         """,
                    ),
                    html.P(
                         """\
                            blah
                         """,
                    )
                ]
                )
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
                html.Div(
                    html.A(
                        "Interactive Tree",
                        id="interactive-tree-link",
                        href='assets/risk_calculators/interactive_tree.html'
                    ),
                    style={'textAlign':"center"}
                )
            ),
            dbc.Col(
                html.Div(
                    html.A(
                        "Interactive Clinical Risk Calculator",
                        id="risk-calculator-link",
                        href='assets/risk_calculators/mortality_app.html'
                    ),
                    style={'textAlign':"center"}
                )
            ),
        ]),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Img(src='assets/risk_calculators/tree.png')
            ]),
        ]),
    ],
    className="page-body"
)

def RickCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout
