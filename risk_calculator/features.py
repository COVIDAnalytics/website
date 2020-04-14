### Data
import datetime
import pandas as pd
import json
### Graphing
import plotly.graph_objects as go
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

with open('risk_calculator/risk_calc_features.json','r') as f:
    features = json.load(f)

def build_dropdown_card(id, content_dict):
    insert_data = \
            [
                dbc.Col(dcc.Markdown("**{}**".format(content_dict['name']))),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id = 'calc-categorical-{}'.format(id),
                            options = [{'label': x, 'value': x} for x in content_dict['vals']],
                            value = "{}".format(content_dict['default']),
                            style={"width":100}
                        ),
                        id = 'calc-categorical-{}-wrapper'.format(id),
                    ),
                ),
            ]
    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target='calc-categorical-{}-wrapper'.format(id),
        ),
    ]
    return card

def build_input_card(id, content_dict):
    insert_data = \
            [
                dbc.Col(dcc.Markdown("**{}**".format(content_dict['name']))),
                dbc.Col(
                    html.Div(
                        dcc.Input(
                            id="calc-numeric-{}".format(id),
                            type="number",
                            placeholder="{}".format(content_dict['default']),
                            style={"width":100}
                        ),
                        id = "calc-numeric-{}-wrapper".format(id)
                    ),
                ),
            ]
    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-numeric-{}-wrapper".format(id),
        ),
    ]
    return card

def build_checkbox_card(id, content_dict):
    insert_data = \
            [
                dbc.Col(dcc.Markdown("**{}**".format(content_dict['name']))),
                dbc.Col(
                    html.Div(
                        dbc.Checklist(
                            options=[{'label': x, 'value': x} for x in content_dict['vals']],
                            value=[],
                            id="calc-checkboxes-{}".format(id),
                        ),
                        id = "calc-checkboxes-{}-wrapper".format(id)
                    ),
                ),
            ]
    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-checkboxes-{}-wrapper".format(id),
        ),
    ]
    return card

def build_feature_cards():
    card_content = []
    cards = []
    inputs = features["numeric"]
    dropdowns = features["categorical"]
    checkboxes = features["checkboxes"]
    for id, content_dict in enumerate(dropdowns):
        card_content.append(build_dropdown_card(id, content_dict))
    for id, content_dict in enumerate(inputs):
        card_content.append(build_input_card(id, content_dict))
    for id, content_dict in enumerate(checkboxes):
        card_content.append(build_checkbox_card(id, content_dict))

    for c in card_content:
        card = \
            dbc.Col(
            [
                dbc.Card(
                    [dbc.CardBody(c,className="feat-options-body")],
                    className="feat-options"
                ),
            ],
            style={
                'paddingBottom':20,
                'borderColor':'red'
                },
            xs=12,
            sm=12,
            md=4,
            lg=4,
            )
        cards.append(card)
    return cards
