import plotly.graph_objects as go
from textwrap import wrap

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from risk_calculator.mortality.calculator import no_labs_features_mort, labs_features_mort, labs_model_mort, no_labs_model_mort
from risk_calculator.infection.calculator import no_labs_features_infec, labs_features_infec, labs_model_infec, no_labs_model_infec
from risk_calculator.utils import fix_title

from navbar import Navbar
from footer import Footer

def build_feature_importance_graph(m=True,labs=False):
    if m:
        model = labs_model_mort if labs else no_labs_model_mort
        features = labs_features_mort if labs else no_labs_features_mort
    else:
        model = labs_model_infec if labs else no_labs_model_infec
        features = labs_features_infec if labs else no_labs_features_infec

    feature_list = ['']*len(model.feature_importances_)
    i = 0
    for feat in features["numeric"]:
        feature_list[feat["index"]] = feat["name"]
        i+=1
    for feat in features["categorical"]:
        feature_list[feat["index"]] = feat["name"]
        i+=1
    for feat in features["checkboxes"]:
        for j,name in enumerate(feat["vals"]):
            feature_list[feat["index"][j]] = name
            i+=1
    for feat in features["multidrop"]:
        for j,name in enumerate(feat["vals"]):
            feature_list[feat["index"][j]] = name
            i+=1
    importances = list(model.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)[:10]
    x,y = zip(*feature_importances)
    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color="#800020"))])
    graph = dcc.Graph(
        id='feature-importance-graph',
        figure=fig,
    )

    fig.update_layout(
                height=450,
                title={
                    'text':'<br>'.join(wrap('<b> Feature Importance Graph </b>', width=30)) ,
                     'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_color='black',
                title_font_size=18,
                xaxis={'title': "Features",'linecolor': 'lightgrey'},
                yaxis={'title': "Importance",'linecolor': 'lightgrey'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )
    return graph


def gender_map(x,name):
    if name == "Sex":
        if x == 0:
            return "Female"
        else:
            return "Male"
    return x

def build_dropdown_card(id, m, content_dict):
    insert_data = \
            [
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id={
                                'type': 'mortality' if m else 'infection',
                                'index': 'calc-categorical-{}'.format(id),
                            },
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

def build_input_card(id, m, content_dict):
    insert_data = \
            [
                dbc.Col(
                    html.Div(
                        dcc.Input(
                            id={
                                'type': 'mortality' if m else 'infection',
                                'index': "calc-numeric-{}".format(id),
                            },
                            type="number",
                            placeholder="e.g. {}".format(int(content_dict['default'])),
                            style={"width":80}
                        ),
                        id = "calc-numeric-{}-wrapper".format(id),
                    ),
                ),
            ]
    if content_dict["name"] == "Temperature Celsius":
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

def build_checkbox_card(id, m, content_dict):
    insert_data = \
            [
                dbc.Col(
                    html.Div(
                        dbc.Checklist(
                            options=[{'label': x, 'value': x} for x in content_dict['vals']],
                            value=[],
                            id={
                                'type': 'mortality' if m else 'infection',
                                'index': "calc-checkboxes-{}".format(id),
                            },
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

def build_multidrop_card(id, m, content_dict):
    insert_data = \
            [
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x} for x in content_dict['vals']],
                            value=[],
                            id={
                                'type': 'mortality' if m else 'infection',
                                'index': "calc-multidrop-{}".format(id)
                            },
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


def build_feature_cards(m=True,labs=False):
    if m:
        features = labs_features_mort if labs else no_labs_features_mort
    else:
        features = labs_features_infec if labs else no_labs_features_infec
    card_content = []
    cards = []
    inputs = features["numeric"]
    dropdowns = features["categorical"]
    multidrop = features["multidrop"]
    for id, content_dict in enumerate(inputs):
        card_content.append((content_dict['name'],build_input_card(str(id),m, content_dict)))
    for id, content_dict in enumerate(dropdowns):
        card_content.append((content_dict['name'],build_dropdown_card(str(id),m, content_dict)))
    if m:
        for id, content_dict in enumerate(multidrop):
            card_content.append((content_dict['name'],build_multidrop_card(str(id),m, content_dict)))

    for name,c in card_content:
        content = dbc.Card(
                        [
                            dbc.CardHeader(fix_title(name),style={"fontWeight": "bold"}),
                            dbc.CardBody(c,className="feat-options-body")
                        ],
                        className="feat-options"
                    )
        w2 = 12 if name == "Comorbidities" else 4
        w1 = 12 if name == "Comorbidities" else 6
        card = \
            dbc.Col([content],
            style={
                'paddingBottom':20,
                'borderColor':'red'
                },
            xs=12,
            sm=w1,
            md=w2,
            lg=w2,
            )
        cards.append(card)
    return cards
