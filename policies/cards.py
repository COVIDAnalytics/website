import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def get_colors():
    return [
                '#000004',
                '#a52c60',
                '#ed6925'
                #'#f7d31d'
            ]

def get_state_num_policy_card(states):
    continents = ["Europe", "Asia", "North America", "South America", "Africa"]
    return [
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [       dcc.Markdown("**For which country and province would you like to project?**"),
                                            dcc.Markdown("**Please select a country and a province, where available.**"),
                                            dbc.Col([dcc.Markdown("**Continent:**"),dcc.Markdown("**Country:**"),dcc.Markdown("**Province / State:**")]),
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                    dcc.Dropdown(
                                                            id = 'continent_policies',
                                                            options = [{'label': x, 'value': x} for x in continents],
                                                            value = 'North America',
                                                    ),
                                                    dcc.Dropdown(
                                                            id = 'country_policies',
                                                    ),

                                                    dcc.Dropdown(
                                                            id = 'province_policies',
                                                    ),
                                                    html.Div(id = "p2-transfer-dropdown-wrapper"),

                                                ]),
                                            ),
                                    ],
                                    justify="center",
                                    style={"paddingBottom":10}
                                ),
                                dbc.Row(
                                    [
                                        dcc.Markdown("Choose up to 3 policies:"),
                                    ],
                                    justify="center",
                                    style={"paddingBottom":0}
                                ),
                            ],
                        ),
                    ],
                    className="projections-general-card h-100",
                    style={
                        'borderWidth': "medium"
                        },
                ),
            ],
            xs=12,
            sm=12,
            md=9,
            lg=6,
            )
        ],
        justify="center",
        style={"paddingBottom":20}
        )
    ]

def timeline_text(t):
    if t==0:
        return "Now"
    elif t < 3:
        return str(t)
    elif t == 3:
        return "4"
    return "6"

def get_policy_card(ind):
    colors = get_colors()
    content = dbc.Card(
                    [
                        dbc.CardHeader(html.H4("Policy {}".format(ind+1),id="policy-header-{}".format(ind)),style={"textAlign": "center"}),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dcc.Markdown("Which policy would you like to implement?"),
                                        dbc.Col(
                                            dcc.Checklist(
                                                id={
                                                    'type': 'none',
                                                    'index': ind,
                                                },
                                                options=[
                                                    {'label': '  No Restrictions', 'value': 'No_Measure', 'disabled': False},
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Checklist(
                                                id={
                                                    'type': 'lockdown',
                                                    'index': ind,
                                                },
                                                options=[
                                                    {'label': '  Lockdown', 'value': 'Lockdown', 'disabled': False},
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                        dbc.Col(
                                            dcc.Checklist(
                                                id={
                                                    'type': 'mass',
                                                    'index': ind,
                                                },
                                                options=[
                                                    {'label': '  Restrict Mass Gatherings', 'value': 'Mass_Gatherings', 'disabled': False},
                                                ],
                                            ),
                                        ),
                                ),
                                dbc.Row(
                                        dbc.Col(
                                            dcc.Checklist(
                                                id={
                                                    'type': 'schools',
                                                    'index': ind,
                                                },
                                                options=[
                                                    {'label': '  Restrict Schools', 'value': 'Schools', 'disabled': True},
                                                ],
                                            ),
                                        ),
                                ),
                                dbc.Row(
                                        dbc.Col(
                                            dcc.Checklist(
                                                id={
                                                    'type': 'others',
                                                    'index': ind,
                                                },
                                                options=[
                                                    {'label': '  Restrict Non-Essential Businesses, Travel Restriction and Workplaces', 'value': 'Others', 'disabled': False},
                                                ],
                                            )
                                        ),
                                ),
                                dbc.Row(
                                    [
                                        html.Div(
                                            id="policy-week-text-{}".format(ind),
                                            style={"paddingBottom": 20, "paddingLeft":10}
                                            ),
                                    ],
                                    style={"paddingTop":10}
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                dcc.Slider(
                                                    min=0,
                                                    max=4,
                                                    marks={i: timeline_text(i) for i in range(5)},
                                                    value=1,
                                                    id={
                                                        'type': 'timeline',
                                                        'index': ind,
                                                    },
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],
                    className="policies-general-card h-100",
                    style={
                        'borderColor': colors[ind],
                        'borderWidth': "medium"
                        },
                )
    card = \
        dbc.Col([content],
        style={
            'paddingBottom':20,
            },
        xs=12,
        sm=12,
        md=4,
        lg=4,
        )
    return card

def get_policy_cards(num_policies):
    return [
                dbc.Row(
                    build_policy_cards(num_policies),
                    id = "policy-cards",
                    justify="center"
                )
            ]

def build_policy_cards(num_policies):
    res = [None] * num_policies
    for i in range(num_policies):
        res[i] = get_policy_card(i)
    return res
