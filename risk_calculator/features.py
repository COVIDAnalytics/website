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

#import feature names
features_name = {}
#import feature types
features_type = {}
#import feature ranges
features_vals = {}
#what will be in placeholder
features_default = {}
#what will be explanation of feature

def fix_category_names(x):
    return x

def build_card_content(key,feat_explanation):
    if features_type[key] == "category"
        insert_data =
                [
                    dbc.Col(dcc.Markdown("**{}**".format(features_name[key]))),
                    dbc.Col(
                        html.Div(
                            dcc.Dropdown(
                                id = 'p1-transfer-dropdown',
                                options = [{'label': fix_category_names(x), 'value': x} for x in features_vals[key]],
                                value = "{}".format(features_default[key]),
                            ),
                            id = "p1-transfer-dropdown-wrapper"
                        ),
                    ),
                ],
    else:
        insert_data =
                [
                    dbc.Col(dcc.Markdown("**{}**".format(name))),
                    dbc.Col(
                        html.Div(
                            dcc.Input(
                                id="input_{}".format(key),
                                type="number",
                                placeholder="{}".format(features_default[key]),
                            ),
                            id = "p1-transfer-dropdown-wrapper"
                        ),
                    ),
                ],


    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            features_explanation[key],
            target="p1-transfer-dropdown-wrapper",
        ),
    ]
    return card


def build_feature_cards():
    cards = [None]*len(features_name.keys())
    for key,name in features_name:
        card = [
            dbc.Col(
            [
                dbc.Card(
                    [dbc.CardBody([build_card_content(features_type[key],features_vals[key])])],
                    className="h-100",
                ),
            ],
            xs=12,
            sm=12,
            md=4,
            lg=4,
            ),
        ]
        cards[key] = card
    return cards
