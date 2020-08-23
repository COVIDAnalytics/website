import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from treatment_calculator.utils import langs, get_title_mapping, labs_ques, oxygen, oxygen_vals



def map_feat_vals(x, name, language):
    if name == "Gender":
        return langs[language].get_gender(x == 0)
    else:
        return name


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
                            'f_idx': content_dict["index"],
                            'feature': feature_name
                        },
                        options=[{'label': map_feat_vals(x, readable_name, language), 'value': x}
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
                        'f_idx': content_dict["index"],
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


def build_checkbox_card(_id, feature_name, feature_index, readable_name):
    item = dbc.Row(
        no_gutters=True,
        style={"width": "100%"},
        children=[
            html.H5(readable_name.split("(")[0], className="input-label", style={"max-width": "250px"}),
            html.Div(
                id='calc-categorical-{}-wrapper'.format(_id),
                style={"width": "100%", "display": "flex", "paddingLeft": "10px"},
                children=[
                    dbc.Checkbox(
                        id={
                            'type': 'treatments',
                            'index': 'calc-checkbox-{}'.format(_id),
                            'f_idx': feature_index,
                            'feature': feature_name
                        },
                        checked=False
                    ),
                    html.H5(readable_name.split("(")[1][0:-1], className="input-label",
                            style={"marginBottom": "0px", "marginLeft": "20px",
                                   "color": "#495057", "fontSize": "15px", "opacity": "1"}),
                ]
            ),
        ]
    )
    return item


def build_multidrop_card(_id, show_name, content_dict, language, feature_name):
    """Used to select multiple from chronic diseases at bottom of mortality calculator"""
    title_mapping = get_title_mapping()
    return dbc.Col([
        html.H5(content_dict["name"], className="input-label",
                style={"display": "inline-block" if show_name else "none"}),
        dcc.Dropdown(
            options=[{'label': title_mapping[language][x], 'value': x} for x in content_dict['vals']],
            value=[],
            id={
                'type': 'treatments',
                'index': "calc-multidrop-{}".format(_id),
                'feature': feature_name
            },
            # Classname needed for tooltip target
            className="dcc_dropdown feature-dropown calc-multidrop-{}".format(_id),
            style={"width": "100%"},
            multi=True,
        ),
        dbc.Tooltip(
            content_dict['explanation'],
            target=".calc-multidrop-{}".format(_id)
        ),
    ])


# TODO: Dropdown tooltips are not translated
def build_feature_cards(features, m=True, labs=False, language=0):
    """This builds all the feature cards"""
    inputs = features["numeric"]
    dropdowns = features["categorical"]
    multidrop = features["multidrop"]
    checkboxes = features["checkboxes"]
    title_mapping = get_title_mapping()

    print(features)

    # The scaffold that will hold ordered feature cards
    feature_scaffold = [
        {
            "group": "Demographics",
            "features": ["age", "gender", "race", "temperature"],
            "mortality": {
                "layout": "2x2",
                "layout_m": "1x3"
            },
        },
        {
            "group": "Metabolic Panel",
            "features": ["alanine amino", "aspartate amino", "bilirubin", "calcium",
                         "creatin", "sodium", "urea nitro", "potas", "glyc"],
            "mortality": {
                "layout": "3x1",
                "layout_m": "4x2",
                "expanded": {
                    "alanine amino": 2,
                    "glyc": 2
                }
            },
            "infection": {
                "expanded": {
                    "alanine amino": [("lg", 2), ("md", 2)], #scale by 2 for large and medium devices
                    "urea nitro": [("lg", 2), ("sm", 2)],
                }
            }
        },
        {
            "group": "Abnormalities",
            "features": [],
            "mortality": {
                "layout": "2x3",
                "vertical_expanded": {
                    "checkboxes": 0.75,
                }
            }
        },
        {
            "group": "Blood Counts",
            # Note: red cell does not exist in mortality calculator, that's why the different dimens
            "features": ["hemoglobin", "lympho", "platelet", "leucocyte"],
            "mortality": {
                "layout": "2x2",
                "layout_m": "2x2",
                "expanded": {
                    "red cell": 2,
                }
            }
        },
        {
            "group": "Other Lab Values",
            "features": ["C-reactive protein", "prothrombin time"],
            "mortality": {
                "layout": "2x1",
                "layout_m": "1x2",
            },
            "infection": {
                "vertical_expanded": {
                    "C-reactive protein": 1.5,
                    "prothrombin time": 1.5
                }
            }
        },
        {
            "group": "Comorbidities",
            "features": ["comorbid"],
            "mortality": {
                "layout": "2x1",
                "layout_m": "1x2",
                "expanded": {
                    "comorbid": 3
                },
                "vertical_expanded": {
                    "comorbid": 2,
                }
            }
        },
        {
            "group": "Unknown",
            "features": [],
            "mortality": {
                "layout": "3x3",
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
                    return
        if feature_name == "checkboxes":
            feature_scaffold[2]["cards"].append((feature_name, feature_card))
            return

        # Add card to default group
        feature_scaffold[-1]["cards"].append((feature_name, feature_card))

    add_feature.count = 0

    for _id, content_dict in enumerate(dropdowns):
        print("Examinign dropdown: " + str(_id))
        add_feature(
            content_dict['name'],
            build_dropdown_card(str(_id), m, content_dict, language, content_dict['name'],
                                title_mapping[language][content_dict['name']])
        )

    for _id, content_dict in enumerate(checkboxes):
        print("Examinign checkbo: " + str(_id))
        for i in range(len(content_dict["vals"])):
            add_feature(
                "checkboxes",
                build_checkbox_card(str(_id),
                                    title_mapping[language][content_dict["vals"][i]],
                                    content_dict["index"][i],
                                    title_mapping[language][content_dict["vals"][i]]
                )
            )

    for _id, content_dict in enumerate(inputs):
        add_feature(
            content_dict['name'],
            # Give different IDs to fix input box not clearing when change
            build_input_card(str(_id) + str(labs), m, content_dict, content_dict['name'],
                             title_mapping[language][content_dict['name']])
        )
    for _id, content_dict in enumerate(multidrop):
        if content_dict['name'] == "Treatments":
            continue
        add_feature(
            content_dict['name'],
            build_multidrop_card(str(_id),
                                 True,
                                  content_dict, language, content_dict['name'])
        )

    # final card layout
    feature_content = []

    # card number to keep track of increasing delay
    card_num = 0

    # Loop through all the groups
    for grp in feature_scaffold:
        # Get the layout dimensions, row x col
        r, c = [int(x) for x in grp["mortality"]["layout"].split('x')]
        r_m, c_m = r, c
        if "layout_m" in grp["mortality"]:
            r_m, c_m = [int(x) for x in grp["mortality"]["layout_m"].split('x')]

        # If there are no cards, skip this group
        if all([x[0] is None for x in grp["cards"]]): continue

        group_content = []

        w = 12 / c
        w_m = 12 / c_m

        # Get all the correct horizontal expansion factors from group
        expansions = {}
        if m and "expanded" in grp["mortality"]:
            expansions = grp["mortality"]["expanded"]
        elif not m:
            if "infection" in grp:
                if "expanded" in grp["infection"]:
                    expansions = grp["infection"]["expanded"]
            elif "expanded" in grp["mortality"]:
                expansions = grp["mortality"]["expanded"]

        # Get all the correct vertical expansion factors from group
        v_expansions = {}
        if m and "vertical_expanded" in grp["mortality"]:
            v_expansions = grp["mortality"]["vertical_expanded"]
        elif not m:
            if "infection" in grp:
                if "vertical_expanded" in grp["infection"]:
                    v_expansions = grp["infection"]["vertical_expanded"]
            elif "vertical_expanded" in grp["mortality"]:
                v_expansions = grp["mortality"]["vertical_expanded"]

        # Loop throgh all the cards in this group
        for name, card in grp["cards"]:
            if name is None:
                continue

            # get expansion factor of this card
            f = {"sm": 1, "md": 1, "lg": 1}
            for n in [ex for ex in expansions if ex.lower() in name.lower()]:
                if type(expansions[n]) == list:
                    for size, scale in expansions[n]:
                        f[size] = scale
                else:
                    f["sm"] = expansions[n]
                    f["md"] = expansions[n]
                    f["lg"] = expansions[n]

            # get vertical expansion factor of this card
            v_f = 1
            for n in [ex for ex in v_expansions if ex.lower() in name.lower()]:
                v_f = v_expansions[n]

            # Create card content and add it to the group content
            group_content.append(dbc.Col(
                xs=12,
                sm=w_m * f["sm"],
                md=w_m * f["md"],
                lg=w * f["lg"],
                style={"padding": "0px"},
                children=dbc.Card(
                    style={"borderRadius": "0px",
                           "height": "{}px".format(str(150 * v_f)),
                           "borderWidth": "1px",
                           "background": "rgba(0, 0, 0, 0)"},
                    children=[
                        dbc.CardBody(card, className="feat-options-body")
                    ])
            ))

        card_num += 1

        # Add the group content to the feature content
        feature_content.append(dbc.Col(
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
        ))
    return feature_content

