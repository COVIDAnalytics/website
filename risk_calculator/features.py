import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

with open('assets/risk_calculators/risk_calc_features.json','r') as f:
    features = json.load(f)

def gender_map(x,name):
    if name == "Gender":
        if x == 0:
            return "Female"
        else:
            return "Male"
    return x

def build_dropdown_card(id, content_dict):
    insert_data = \
            [
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id = 'calc-categorical-{}'.format(id),
                            options = [{'label': gender_map(x,content_dict["name"]), 'value': x} for x in content_dict['vals']],
                            value = 0,
                            style={"width":110}
                        ),
                        id = 'calc-categorical-{}-wrapper'.format(id),
                    ),
                ),
            ]
    card = [
        dbc.Row(
            insert_data,
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
                dbc.Col(
                    html.Div(
                        dcc.Input(
                            id="calc-numeric-{}".format(id),
                            type="number",
                            placeholder="e.g. {}".format(int(content_dict['default'])),
                            style={"width":80}
                        ),
                        id = "calc-numeric-{}-wrapper".format(id),
                    ),
                ),
            ]
    if content_dict["name"] == "Body Temperature":
        insert_data.append(
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id = 'calc-temp-f-c',
                        options = [{'label': x, 'value': x} for x in ["°F","°C"]],
                        value = "°F",
                        style={"width":70}
                    ),
                ),
            ),
        )
    card = [
        dbc.Row(
            insert_data,
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
                dbc.Col(
                    html.Div(
                        dbc.Checklist(
                            options=[{'label': x, 'value': x} for x in content_dict['vals']],
                            value=[],
                            id="calc-checkboxes-{}".format(id),
                        ),
                        id = "calc-checkboxes-{}-wrapper".format(id),
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

def build_multidrop_card(id, content_dict):
    insert_data = \
            [
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x} for x in content_dict['vals']],
                            value=[],
                            id="calc-multidrop-{}".format(id),
                            multi=True,
                        )],
                        id = "calc-multidrop-{}-wrapper".format(id),
                    )
                ),
            ]
    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-multidrop-{}-wrapper".format(id),
        ),
    ]
    return card

def build_feature_cards():
    card_content = []
    cards = []
    inputs = features["numeric"]
    dropdowns = features["categorical"]
    checkboxes = features["checkboxes"]
    multidrop = features["multidrop"]
    for id, content_dict in enumerate(dropdowns):
        card_content.append((content_dict['name'],build_dropdown_card(id, content_dict)))
    for id, content_dict in enumerate(inputs):
        card_content.append((content_dict['name'],build_input_card(id, content_dict)))
    for id, content_dict in enumerate(checkboxes):
        card_content.append((content_dict['name'],build_checkbox_card(id, content_dict)))
    for id, content_dict in enumerate(multidrop):
        card_content.append((content_dict['name'],build_multidrop_card(id, content_dict)))

    for name,c in card_content:
        content = dbc.Card(
                        [
                            dbc.CardHeader(name,style={"fontWeight": "bold"}),
                            dbc.CardBody(c,className="feat-options-body")
                        ],
                        className="feat-options"
                    )
        w = 12 if name == "Comorbidities" else 4
        card = \
            dbc.Col([content],
            style={
                'paddingBottom':20,
                'borderColor':'red'
                },
            xs=12,
            sm=w,
            md=w,
            lg=w,
            )
        cards.append(card)
    return cards
