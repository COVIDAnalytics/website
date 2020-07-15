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
    return "Chungus"


def build_dropdown_card(_id, m, content_dict, language, feature_name, readable_name):
    """Makes feature card with dropdown data"""
    insert_data = [
        dbc.Col(
           children=[
                html.H5(readable_name, className="input-label"),
                html.Div(
                    id='calc-categorical-{}-wrapper'.format(_id),
                    children=dcc.Dropdown(
                        id={
                            'type': 'mortality' if m else 'infection',
                            'index': 'calc-categorical-{}'.format(_id),
                            'feature': feature_name
                        },
                        options=[{'label': map_feat_vals(x, content_dict["name"], language), 'value': x}
                                 for x in content_dict['vals']],
                        value=0,
                        className="dcc_dropdown feature-dropdown",
                        clearable=False,
                    ),
                ),
            ]
        ),
    ]
    card = [
        dbc.Row(
            insert_data,
            no_gutters=True,
            style={"width": "100%"}
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
        'feature': "SaO2"  # This is the no_labs version of oxygen saturation (index 8), as opposed to
        # ABG: Oxygen Saturation (SaO2) which is the labs version of it (index 2)
    }
    if have_val:
        label = text[0]
        small_label = False
        content = dbc.Input(
            id=id_full,
            type="number",
            placeholder="e.g. 92",
            className="numeric-input",
            bs_size="lg"
        )
    else:
        label = text[1]
        small_label = True
        content = dcc.Dropdown(
            id=id_full,
            options=[{'label': oxygen_vals(x, language), 'value': x} for x in [92, 98]],
            value=98,
            style={"width": 80},
            className="dcc_dropdown",
            clearable=False
        )
    return [
        html.Div(html.H5(label,
                         className="input-label",
                         style={"height": "48px"} if small_label else {}),
                 style={"textAlign": "end"}),
        dbc.Row(
            content,
            align="end",
            justify="end",
            no_gutters=True,
        ),
    ]


def build_oxygen_card(_id, labs, m, content_dict, language):
    """Oxygen Saturation Card and Top Input Builder (Builds card and uppper text and dropdowns of last card.)"""
    model = 'mortality' if m else 'infection'
    lab_str = "labs" if labs else "nolabs"
    card = [
        dbc.Row(
            style={"width": "100%"},
            children=[
                dbc.Col(children=[
                    html.H5(langs[language].hasO2Value, className="input-label",
                            style={"fontSize": "15px", "height": "36px"}),
                    dcc.Dropdown(
                        id="oxygen-answer-{}".format(model),
                        options=[{'label': labs_ques(x, language), 'value': x} for x in [1, 0]],
                        value=0,
                        style={"width": 80},
                        className="dcc_dropdown",
                        clearable=False
                    )
                ]),
                dbc.Col(
                    align="end",
                    # This is a wrapper. The return value of oxygen_options gets placed into here when the
                    # get_oxygen_infection/mortality callback gets invoked
                    id="calc-numeric-{}-wrapper-{}-{}".format(_id, model, lab_str),
                )
            ]
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-numeric-{}-wrapper-{}-{}".format(_id, model, lab_str),
        ),
    ]
    return card


def build_input_card(_id, m, content_dict, feature_name, readable_name):
    is_temp = content_dict["name"] == "Body Temperature"
    insert_data = [
        dbc.Col([
            html.H5(readable_name, className="input-label"),
            html.Div(
                id="calc-numeric-{}-wrapper".format(_id),
                children=dbc.Input(
                    id={
                        'type': 'mortality' if m else 'infection',
                        'index': "calc-numeric-{}".format(_id),
                        'feature': feature_name
                    },
                    type="number",
                    placeholder="e.g. {}".format(int(content_dict['default'])),
                    className="numeric-input " + "temp-input" if is_temp else "",
                    bs_size="lg"
                ),
            ),
        ], align="stretch"
        ),
    ]
    if is_temp:
        insert_data.append(
            dcc.Dropdown(
                id={
                    'type': 'temperature',
                    'index': "units",
                },
                options=[{'label': x, 'value': x} for x in ["°F", "°C"]],
                value="°F",
                className="dcc_dropdown temp-dropdown",
                clearable=False
            ),

        )
    card = [
        dbc.Row(
            insert_data,
            align="end",
            no_gutters=True,
            style={"width": "100%"}
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-numeric-{}-wrapper".format(_id),
        ),
    ]
    return card


# TODO: This function is not being used anywhere (no checkbox cards). Kill it?
def build_checkbox_card(_id, m, content_dict, feature_name):
    card = [
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="calc-checkboxes-{}-wrapper".format(_id),
                    children=dbc.Checklist(
                        options=[{'label': x, 'value': x} for x in content_dict['vals']],
                        value=[],
                        id={
                            'type': 'mortality' if m else 'infection',
                            'index': "calc-checkboxes-{}".format(_id),
                            'feature': feature_name
                        },
                    ),
                ),
            ),
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target="calc-checkboxes-{}-wrapper".format(_id),
        ),
    ]
    return card


def build_multidrop_card(_id, m, content_dict, language, feature_name):
    """Used to select multiple from chronic diseases at bottom of mortality calculator"""
    title_mapping = get_title_mapping()
    return [
        dcc.Dropdown(
            options=[{'label': title_mapping[language][x], 'value': x} for x in content_dict['vals']],
            value=[],
            id={
                'type': 'mortality' if m else 'infection',
                'index': "calc-multidrop-{}".format(_id),
                'feature': feature_name
            },
            # Classname needed for tooltip target
            className="dcc_dropdown calc-multidrop-{}".format(_id),
            style={"width": "100%"},
            multi=True,
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

    print(features)

    # The scaffold that will hold ordered feature cards
    feature_scaffold = [
        {
            "group": "Demographics",
            "features": ["age", "gender"],
            "mortality": {
                "layout": "2x1",
                "layout_m": "1x2"
            },
        },
        {
            "group": "Vitals",
            "features": ["body temp", "cardiac freq", "SaO2", "respiratory freq"],
            "mortality": {
                "layout": "2x2",
                "expanded": {
                    "SaO2": 2  # Expand Sao2 card by a factor of 2
                }
            }
        },
        {
            "group": "Metabolic Panel",
            "features": ["alanine amino", "aspartate amino", "bilirubin", "calcium",
                         "creatin", "sodium", "urea nitro", "potas"],
            "mortality": {
                "layout": "3x3",
                "layout_m": "4x2",
                "expanded": {
                }
            }
        },
        {
            "group": "Blood Counts",
            # Note: red cell does not exist in mortality calculator, that's why the different dimens
            "features": ["hemoglobin", "leukocytes", "mean corpuscular", "platelet", "red cell"],
            "mortality": {
                "layout": "2x2",
                "layout_m": "2x2",
            }
        },
        {
            "group": "Misc.",
            "features": ["C-reactive protein", "prothrombin time"],
            "mortality": {
                "layout": "2x1",
                "layout_m": "1x2"
            }
        },
        {
            "group": "Comorbidities",
            "features": ["comorbid"],
            "mortality": {
                "layout": "1x3",
                "layout_m": "1x2",
                "expanded": {
                    "comorbid": 3
                }
            }
        },
        {
            "group": "Unknown",
            "features": [],
            "mortality": {
               "layout": "3x3"
            }
        }
    ]
    for group in feature_scaffold:
            group["cards"] = [(None, [])] * len(group["features"])
    feature_scaffold[-1]["cards"] = []

    # Add a card into its right place in the scaffold
    def add_feature(feature_name, feature_card):
        add_feature.count += 1
        # Try to add card to its appropraite group
        for grp in enumerate(feature_scaffold):
            # Check if name is in this group's features
            for fname in enumerate(grp[1]["features"]):
                if fname[1].lower() in feature_name.lower():
                    feature_scaffold[grp[0]]["cards"][fname[0]] = (feature_name, feature_card)
                    print("Adding: " + feature_name + " to " + str(grp[1]))
                    return
        print("Adding: " + feature_name + " to OTHER")
        # Add card to default group
        feature_scaffold[-1]["cards"].append((feature_name, feature_card))

    add_feature.count = 0

    for _id, content_dict in enumerate(dropdowns):
        add_feature(
            content_dict['name'],
            build_dropdown_card(str(_id), m, content_dict, language, content_dict['name'],
                                title_mapping[language][content_dict['name']])
        )
    for _id, content_dict in enumerate(inputs):
        if not labs and title_mapping[0][content_dict['name']] == oxygen:
            add_feature(
                content_dict['name'],
                build_oxygen_card(str(_id), labs, m, content_dict, language)
            )
        else:
            print("Adding feature: " + content_dict['name'])
            add_feature(
                content_dict['name'],
                build_input_card(str(_id), m, content_dict, content_dict['name'],
                                 title_mapping[language][content_dict['name']])
            )
    if m:
        for _id, content_dict in enumerate(multidrop):
            add_feature(
                content_dict['name'],
                build_multidrop_card(str(_id), m, content_dict, language, content_dict['name'])
            )

    '''
    # 2, 4, 7, 5, 2, 1
    LEN             | MOBILE
    - length: 2 
        #           # # 
        #
    - length: 4
          # #       ###  
          ###       ###     (oxygen
          # #       # #     
    - length: 5
        ### #       ### 
        # # #       # #  
                    # #
    - length: 7     
        ### #       ### 
        # # #       # #
        # ###       # #
                    # #
    - length: 2
        #           # #
        #           
    - length: 1     
          ###       ###     (comobirtides)
          ###
    '''

    card_num = 0
    for grp in feature_scaffold:
        if "mortality" not in grp: continue
        r, c = [int(x) for x in grp["mortality"]["layout"].split('x')]
        r_m, c_m = r, c
        if "layout_m" in grp["mortality"]:
            r_m, c_m = [int(x) for x in grp["mortality"]["layout_m"].split('x')]
        if all([x[0] is None for x in grp["cards"]]): continue
        group_content = []

        w = 12 / c
        w_m = 12 / c_m
        for name, card in grp["cards"]:
            if name is None:
                continue

            f = 1
            expansions = []
            if m and "expanded" in grp["mortality"]:
                expansions = grp["mortality"]["expanded"]
            elif not m and "expanded" in grp["infection"]:
                expansions = grp["mortality"]["expanded"]
            for n in [ex for ex in expansions if ex.lower() in name.lower()]:
                f = expansions[n]

            content = dbc.Col(
                xs=12,
                sm=w_m * f,
                md=w_m * f,
                lg=w * f,
                style={"padding": "0px"},
                children=dbc.Card(
                    style={"borderRadius": "0px",
                           "height": "150px",
                           "borderWidth": "1px",
                           "background": "rgba(0, 0, 0, 0)"},
                    children=[
                        dbc.CardBody(card, className="feat-options-body")
                    ])
            )

            group_content.append(content)

        card_num += 1
        group_card = dbc.Col(
            style={
                'paddingBottom': 30,
                'borderColor': 'red',
            },
            xs=12,
            sm=c_m * 6,
            md=c_m * 6,
            lg=c * 4,
            children=[
                html.Div(
                    **{"data-aos": "fade-up", "data-aos-delay": str(card_num % 4 * 150)},
                    # For overlapping dropdown problem
                    style={"transformStyle": "flat",
                           "zIndex": str(add_feature.count - card_num),
                           "position": "relative"},
                    className="aos-refresh-onload",
                    children=dbc.Card(
                        className="elevation-3",
                        style={"borderWidth": "0px"},
                        children=[
                            dbc.CardHeader(grp["group"],
                                           style={"fontWeight": "bold"}),
                            dbc.Row(group_content, style={"margin": "0px", "borderWidth": "0px"})
                        ]
                    )
                )
            ],
        )
        cards.append(group_card)
    return cards

