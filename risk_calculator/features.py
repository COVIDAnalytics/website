import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from risk_calculator.utils import langs, get_title_mapping, labs_ques, oxygen, oxygen_vals


def build_feature_importance_graph(m=True, labs=False):
    """Returns the correct graph image. m=Mortality Graph?, labs=With lab values?"""
    image = 'assets/risk_calculators/'
    if m:
        image += 'mortality/model_with_lab.jpg' if labs else 'mortality/model_without_lab.jpg'
    else:
        image += 'infection/model_with_lab.jpg' if labs else 'infection/model_without_lab.jpg'
    return [dbc.CardImg(src=image)]


def map_feat_vals(x, name, language):
    if name == "Gender":
        return langs[language].get_gender(x == 0)
    return x


def build_dropdown_card(_id, m, content_dict, language):
    insert_data = [
        dbc.Col(
            html.Div(
                id='calc-categorical-{}-wrapper'.format(_id),
                children=dcc.Dropdown(
                    id={
                        'type': 'mortality' if m else 'infection',
                        'index': 'calc-categorical-{}'.format(_id),
                    },
                    options=[{'label': map_feat_vals(x, content_dict["name"], language), 'value': x}
                             for x in content_dict['vals']],
                    value=0,
                    style={"width": 110}
                ),
            ),
        ),
    ]
    card = [
        dbc.Row(
            insert_data,
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target='calc-categorical-{}-wrapper'.format(_id),
        ),
    ]
    return card


def oxygen_options(_id, m, have_val, text, language):
    """Oxygen Saturation Card Builder (last card. Shows different inputs whether user has oxygen vals or not)"""
    id_full = {
        'type': 'mortality' if m else 'infection',
        'index': "calc-numeric-{}".format(_id),
    }
    if have_val:
        return [
            dbc.Col(
                html.Div(text[0]),
            ),
            dbc.Col(
                dcc.Input(
                    id=id_full,
                    type="number",
                    placeholder="e.g. 92",
                    style={"width": 80}
                )
            )
        ]
    else:
        return [
            dbc.Col(
                html.Div(text[1]),
            ),
            dbc.Col(
                dcc.Dropdown(
                    id=id_full,
                    options=[{'label': oxygen_vals(x, language), 'value': x} for x in [92, 98]],
                    value=98,
                    style={"width": 80}
                ),
            )
        ]


def build_oxygen_card(_id, labs, m, content_dict, language):
    model = 'mortality' if m else 'infection'
    lab_str = "labs" if labs else "nolabs"
    insert_data = [
        dbc.Row([
            dbc.Col(html.Div(langs[language].hasO2Value)),
            dbc.Col(
                dcc.Dropdown(
                    id="oxygen-answer-{}".format(model),
                    options=[{'label': labs_ques(x, language), 'value': x} for x in [1, 0]],
                    value=0,
                    style={"width": 80}
                ),
            )
        ]),
        dbc.Row(
            id="calc-numeric-{}-wrapper-{}-{}".format(_id, model, lab_str),
        )
    ]

    card = [
        dbc.Row(
            insert_data,
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-numeric-{}-wrapper-{}-{}".format(_id, model, lab_str),
        ),
    ]
    return card


def build_input_card(_id, m, content_dict):
    insert_data = [
        dbc.Col(
            html.Div(
                id="calc-numeric-{}-wrapper".format(_id),
                children=dcc.Input(
                    id={
                        'type': 'mortality' if m else 'infection',
                        'index': "calc-numeric-{}".format(_id),
                    },
                    type="number",
                    placeholder="e.g. {}".format(int(content_dict['default'])),
                    style={"width": 90}
                ),
            ),
        ),
    ]
    if content_dict["name"] == "Body Temperature":
        insert_data.append(
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id={
                            'type': 'temperature',
                            'index': "units",
                        },
                        options=[{'label': x, 'value': x} for x in ["°F", "°C"]],
                        value="°F",
                        style={"width": 80}
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
            target="calc-numeric-{}-wrapper".format(_id),
        ),
    ]
    return card


# TODO: This function is not being used anywhere (no checkbox cards). Kill it?
def build_checkbox_card(_id, m, content_dict):
    insert_data = [
        dbc.Col(
            html.Div(
                id="calc-checkboxes-{}-wrapper".format(_id),
                children=dbc.Checklist(
                    options=[{'label': x, 'value': x} for x in content_dict['vals']],
                    value=[],
                    id={
                        'type': 'mortality' if m else 'infection',
                        'index': "calc-checkboxes-{}".format(_id),
                    },
                ),
            ),
        ),
    ]
    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-checkboxes-{}-wrapper".format(_id),
        ),
    ]
    return card


def build_multidrop_card(_id, m, content_dict, language):
    """Used to select multiple from chronic diseases at bottom of mortality calculator"""
    title_mapping = get_title_mapping()
    insert_data = [
        dbc.Col(
            html.Div(
                id="calc-multidrop-{}-wrapper".format(_id),
                children=dcc.Dropdown(
                    options=[{'label': title_mapping[language][x], 'value': x} for x in content_dict['vals']],
                    value=[],
                    id={
                        'type': 'mortality' if m else 'infection',
                        'index': "calc-multidrop-{}".format(_id)
                    },
                    multi=True
                ),
            )
        ),
    ]
    card = [
        dbc.Row(
            insert_data
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-multidrop-{}-wrapper".format(_id),
        ),
    ]
    return card


# TODO: Dropdown tooltips are not translated
def build_feature_cards(features, m=True, labs=False, language=0):
    """This builds all the feature cards"""
    card_content = []
    cards = []
    inputs = features["numeric"]
    dropdowns = features["categorical"]
    multidrop = features["multidrop"]
    title_mapping = get_title_mapping()
    for _id, content_dict in enumerate(dropdowns):
        card_content.append((
            content_dict['name'],
            build_dropdown_card(str(_id), m, content_dict, language)
        ))
    for _id, content_dict in enumerate(inputs):
        if not labs and title_mapping[0][content_dict['name']] == oxygen:
            card_content.append((
                content_dict['name'],
                build_oxygen_card(str(_id), labs, m, content_dict, language)
            ))
        else:
            card_content.append((
                content_dict['name'], build_input_card(str(_id), m, content_dict)
            ))
    if m:
        for _id, content_dict in enumerate(multidrop):
            card_content.append((
                content_dict['name'], build_multidrop_card(str(_id), m, content_dict, language)
            ))

    for name, c in card_content:
        content = dbc.Card([
            dbc.CardHeader(title_mapping[language][name], style={"fontWeight": "bold"}),
            dbc.CardBody(c, className="feat-options-body")
        ], className="feat-options")

        if name == "Comorbidities":
            w2 = 12
            w1 = 12
        elif not labs and title_mapping[0][name] == oxygen:
            w2 = 6
            w1 = 12
        else:
            w2 = 3
            w1 = 6
        card = dbc.Col(
            [content],
            style={
                'paddingBottom': 20,
                'borderColor': 'red'
                },
            xs=w1,
            sm=w1,
            md=w1,
            lg=w2,
        )
        cards.append(card)
    return cards
