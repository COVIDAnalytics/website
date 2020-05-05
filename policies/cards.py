import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def get_state_num_policy_card(states):
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
                                    [
                                        dcc.Markdown("For which state would you like to project?"),
                                        dbc.Col(
                                            html.Div(
                                                dcc.Dropdown(
                                                    id = 'state_policies',
                                                    options = [{'label': x, 'value': x} for x in states],
                                                    value = 'New York',
                                                ),
                                                id = "p2-transfer-dropdown-wrapper",
                                            ),
                                        width=6,
                                        style={"paddingBottom":20}
                                        ),
                                    ],
                                    justify="center"
                                ),
                                dbc.Row(
                                    [
                                        dcc.Markdown("How many policies would you like to project?"),
                                    ],
                                    justify="center"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                dcc.Dropdown(
                                                    id = 'amount_policies',
                                                    options = [{'label': x, 'value': x} for x in [1,2,3,4]],
                                                    value = 1,
                                                ),
                                                id = "p2-transfer-dropdown-wrapper",
                                            ),
                                        width="auto"
                                        ),
                                    ],
                                    justify="center"
                                ),
                            ],
                        ),
                    ],
                    className="projections-general-card h-100",
                ),
            ],
            xs=12,
            sm=12,
            md=9,
            lg=6,
            )
        ],
        justify="center"
        )
    ]

def timeline_text(t):
    if t==0:
        return "Now"
    else:
        return "In {} Weeks".format(t)

def get_state_num_policy_card(ind):
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
                                    [
                                        dcc.Markdown("Which policy would you like to implement?"),
                                        dbc.Col(
                                            html.Div(
                                                dcc.RadioItems(
                                                    id="radio-lockdown-policy-{}".format(ind),
                                                    options=[
                                                        {'label': 'Lockdown', 'value': 'Lockdown',},
                                                    ],
                                                ),
                                                dcc.RadioItems(
                                                    id="radio-mass-policy-{}".format(ind),
                                                    options=[
                                                        {'label': 'Restrict Mass Gatherings', 'value': 'Mass_Gatherings'},
                                                    ],
                                                ),
                                                dcc.RadioItems(
                                                    id="radio-schools-policy-{}".format(ind),
                                                    options=[
                                                        {'label': 'Restrict Schools', 'value': 'Schools'},
                                                    ],
                                                ),
                                                dcc.RadioItems(
                                                    id="radio-others-policy-{}".format(ind),
                                                    options=[
                                                        {'label': 'Restrict Non-Essential Businesses, Travel Restriction and Workplaces', 'value': 'Others'},
                                                    ],
                                                ) ,
                                                id = "p2-transfer-dropdown-wrapper",
                                            ),
                                        width=6,
                                        style={"paddingBottom":20}
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dcc.Markdown("When would you like it implemented?"),
                                    ],
                                    justify="center"
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
                                                    id="slider-policy-{}".format(ind)
                                                ),
                                                id = "p2-transfer-dropdown-wrapper",
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                    className="projections-general-card h-100",
                ),
            ],
            xs=12,
            sm=12,
            md=9,
            lg=6,
            )
        ],
        justify="center"
        )
    ]
