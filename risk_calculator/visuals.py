import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def labs_ques(val):
    return "Yes" if val else "No"

def get_labs_indicator(id):
    return  [
                dbc.Row(
                [
                    dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Markdown("Do you have lab values?"),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                        dcc.Dropdown(
                                                                id = id,
                                                                options = [{'label': labs_ques(x), 'value': x} for x in [1,0]],
                                                                value = 0,
                                                        ),

                                                    ]),
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ],
                            className="projections-general-card h-100"
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=6,
                    lg=6,
                    ),
                ],
                justify="center",
                style={"paddingBottom":20}
                ),
            ]

def get_model_desc(id):
    return [
                dbc.Row(
                [
                    dbc.Col(
                    [
                        html.Div(
                            id = id
                        )
                    ],
                    ),
                ]
                ),
            ]

def get_feature_importance(id):
    return [
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(
                                id = id,
                                style={"paddingTop":20,"paddingBottom":20}
                            )
                        ],
                    ),
                    justify="center",
                ),
            ]

def get_feature_cards(id):
    return [
                dbc.Row(
                [
                    dbc.Col(
                        html.H5('Insert the features below into the risk calculator.')
                    ),
                ]),
                dbc.Row(
                    id = id,
                    justify="center"
                )
            ]

def get_submit_button(id):
    return [
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            dbc.Button(
                                "Submit",
                                id=id,
                                n_clicks=0,
                                className="mr-1"
                            ),
                        id="submit-features-calc-wrapper",
                        )
                    ),
                ),
            ]

def get_results_card(id,err_id):
    return [
                dbc.Row(
                    dbc.Col(
                        [
                        dcc.ConfirmDialog(
                            id=err_id,
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(id=id)
                            ],
                            color="dark",
                            inverse=True,
                            style={"marginTop":20,"marginBottom":20}
                            ),
                        ],
                        xs=12,
                        sm=6,
                        md=6,
                        lg=3,
                    ),
                    justify="center",
                )
            ]

def get_inputed_vals(id):
    return [
                dbc.Row(
                    dbc.Col(
                    [
                        dcc.Markdown(
                            id = id
                        )
                    ],
                    ),
                    justify="center",
                ),
            ]
