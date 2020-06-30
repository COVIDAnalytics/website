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
    """Makes feature card with dropdown data"""
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
                    style={"width": 110},
                    className="dcc_dropdown",
                    clearable=False,
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
    """Oxygen Saturation BOttom Input Builder (Builds only the bottom text and dropdowns of last card.
    Shows different inputs whether user has oxygen vals or not)"""
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
                    style={"width": 80},
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
                    style={"width": 80},
                    className="dcc_dropdown",
                    clearable=False
                ),
            )
        ]


def build_oxygen_card(_id, labs, m, content_dict, language):
    """Oxygen Saturation Card and Top Input Builder (Builds card and uppper text and dropdowns of last card.)"""
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
                    style={"width": 80},
                    className="dcc_dropdown",
                    clearable=False
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
                        style={"width": 80},
                        className="dcc_dropdown",
                        clearable=False
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
    return [
        dcc.Dropdown(
            options=[{'label': title_mapping[language][x], 'value': x} for x in content_dict['vals']],
            value=[],
            id={
                'type': 'mortality' if m else 'infection',
                'index': "calc-multidrop-{}".format(_id)
            },
            className="dcc_dropdown calc-multidrop-{}".format(_id),
            multi=True
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target=".calc-multidrop-{}".format(_id)
        ),
    ]


# TODO: Dropdown tooltips are not translated
def build_feature_cards(features, m=True, labs=False, language=0):
    """This builds all the feature cards"""
    cards = []
    inputs = features["numeric"]
    dropdowns = features["categorical"]
    multidrop = features["multidrop"]
    title_mapping = get_title_mapping()

    # The scaffold that will hold ordered feature cards
    feature_scaffold = [
        {
            "group": "Vitals",
            "features": ["age", "gender", "temp", "cardiac freq"],
        },
        {
            "group": "Bloodwork",
            "features": ["SaO2", "CRP", "BUN", "sodium"],
        },
        {
            "group": "Other",
            "features": []
        }
    ]
    for group in feature_scaffold:
        group["cards"] = [(None, [])] * len(group["features"])

    # Add a card into its right place in the scaffold
    def add_feature(feature_name, feature_card):
        # Try to add card to its appropraite group
        for grp in enumerate(feature_scaffold):
            # Check if name is in this group's features
            for fname in enumerate(grp[1]["features"]):
                if fname[1].lower() in feature_name.lower():
                    feature_scaffold[grp[0]]["cards"][fname[0]] = (feature_name, feature_card)
                    return
        # Add card to default group
        feature_scaffold[-1]["cards"].append((feature_name, feature_card))

    # Loop over all features from the json and add the to the scaffold
    for _id, content_dict in enumerate(dropdowns):
        add_feature(
            content_dict['name'],
            build_dropdown_card(str(_id), m, content_dict, language)
        )
    for _id, content_dict in enumerate(inputs):
        if not labs and title_mapping[0][content_dict['name']] == oxygen:
            add_feature(
                content_dict['name'],
                build_oxygen_card(str(_id), labs, m, content_dict, language)
            )
        else:
            add_feature(
                content_dict['name'],
                build_input_card(str(_id), m, content_dict)
            )
    if m:
        for _id, content_dict in enumerate(multidrop):
            add_feature(
                content_dict['name'],
                build_multidrop_card(str(_id), m, content_dict, language)
            )

    card_num = 0

    # Loop through all cards in the scaffold in order using nested list comprehension :-)
    for name, feature_card in [feature for grp in feature_scaffold for feature in grp["cards"]]:

        # Skip unpopulated cards
        if name is None:
            continue

        print(name)
        content = html.Div(
            **{"data-aos": "fade-up", "data-aos-delay": str(card_num % 4 * 150), "data-aos-mirror": "true"},
            className="",
            children=dbc.Card([
                dbc.CardHeader(title_mapping[language][name], style={"fontWeight": "bold"}),
                dbc.CardBody(feature_card, className="feat-options-body")
            ], className="feat-options")
        )

        if name == "Comorbidities":
            w2 = 6
            w1 = 12
        elif not labs and title_mapping[0][name] == oxygen:
            w2 = 6
            w1 = 12
        else:
            w2 = 3
            w1 = 6
        cards.append(dbc.Col(
            [content],
            id=name+"-labs" if labs else name,
            style={
                'paddingBottom': 20,
                'borderColor': 'red'
                },
            xs=w1,
            sm=w1,
            md=w1,
            lg=w2,
        ))
        cards.append(html.Div(style={"display": "none"}, id=name if labs else name + "-labs"))
        card_num += 1
    return cards
