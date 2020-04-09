import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

from ventilators.utils import models

transfers_table = \
[
    dbc.Row(
        [
            dbc.Col(
            [
                html.Div(id='table-text',children='',style={'paddingTop':"20px"}),
            ]
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Transfer:',id="date-projections"),
            ]
            ),
            dbc.Col(
            [
                html.Div(
                    dcc.Dropdown(
                        id = 'transfer-to-from-dropdown',
                        options = [{'label': x, 'value': x} for x in ["to", "from"]],
                        value = 'to',
                    ),
                ),
            ]
            ),
            dbc.Col(
            [
                html.Div(
                    dcc.Dropdown(
                        id = 'transfer-state-dropdown',
                        options = [{'label': x, 'value': x} for x in models],
                        value = '',
                    ),
                    style={'textAlign':"center"}
                ),
            ]
            ),
        ],
        ),
        dbc.Row([
            dbc.Col(
            [

            ]
            ),
        ],
        ),
        dbc.Row([
            dbc.Col(
            [
                html.Div(id='table-container')
            ],
            ),
        ],
        ),
    ]
