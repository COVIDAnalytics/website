### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from navbar import Navbar
from footer import Footer
import yaml

nav = Navbar()
footer = Footer()

# Load team members
with open("assets/team_members/team.yml") as f:
    members = yaml.load(f, Loader=yaml.FullLoader)
num_members = len(members)
members_per_row = 4


# Single member pic
def member_pic(member):
    return dbc.Col(
        [
            html.Div(
            [
                html.Img(src='assets/team_members/photos/%s' % member['photo']),
                dbc.Button(
                    member['name'],
                    color="info",
                    block=True,
                    className="mb-3",
                    href=member['website'])
             ],
             style={'display': 'inline-block'}
            )
        ],
        width=True,
    )

# Table rows
member_rows = \
    [
        dbc.Row(
            [
                member_pic(members[0])
            ],
        )
    ] + \
    [
        dbc.Row(
            [
                member_pic(m) for m in members[1 + i*members_per_row:1 + (i+1)*members_per_row]
            ]
        ) for i in range(num_members//members_per_row)
    ] + \
    [
        dbc.Row(
            [
                member_pic(m) for m in members[1 + num_members - (num_members % members_per_row):]
            ]
        )
    ]

body = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                    [
                        html.H2("Our Team"),
                        html.P('Our team comprises passionate researchers in Operations Research \
                        and Analytics. We were eager to use our collective skills and create new \
                        tools that can help the scientific community fight against the pandemic.')
                    ]
                    )
                ],
                style={'margin-bottom': 20}
            )
        ] + member_rows,
        className="page-body"
    )

def Team():
    layout = html.Div([nav, body, footer],className="site")
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Team()
app.title = "COVIDAnalytics"
