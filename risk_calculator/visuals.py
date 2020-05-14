import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from risk_calculator.utils import labs_ques


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
                                        dcc.Markdown(id=id+"_text"),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                        dcc.Dropdown(
                                                                id = id,
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
                    dbc.Jumbotron(
                            id = id,
                            style={'paddingBottom':'0.5rem','paddingTop':'0.8rem'}
                    ),
                ],
                justify="center"
                ),
            ]

def get_feature_importance(id):
    return [
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Card(
                                id = id,
                                style={"borderColor": "#800020","paddingTop":20,"paddingBottom":20},
                            ),
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
                        id = id+"-text",
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
                    [
                        dbc.Col(
                            html.Div(
                                dbc.Button(
                                    id=id,
                                    n_clicks=0,
                                    className="mr-1"
                                ),
                            id="submit-features-calc-wrapper",
                            )
                        ),
                    ],
                    style = {"paddingBottom":10}
                ),
            ]

def get_results_card(id,err_id):
    return [
                dbc.Row(
                    dbc.Col(
                        [
                            html.P(
                                id=err_id,
                                style={"color":"red","textAlign":"center"}
                            )
                        ],
                        xs=12,
                        sm=12,
                        md=12,
                        lg=12,
                    ),
                    justify="center",
                ),
                dbc.Row(
                    dbc.Col(
                        [
                        dbc.Card(
                            [
                                dbc.CardBody(id=id)
                            ],
                            color="dark",
                            inverse=True,
                            style={"marginTop":10,"marginBottom":20}
                            ),
                        ],
                        xs=12,
                        sm=6,
                        md=6,
                        lg=3,
                    ),
                    justify="center",
                ),
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


def get_personal_visual(id):
    return [
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dcc.Markdown(id=id+"-explanation"),
                                    html.Img(
                                        id = id,
                                        style={"height":200}
                                    ),
                                ],
                                style={
                                    "borderColor": "white",
                                    }
                            )
                        ],
                    ),
                    justify="center",
                ),
            ]

language_ind = {
    0: "English",
    1: "Español",
    2: "Italiano"
}

def get_lang(id):
    return [
        dbc.Row(
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id = id,
                        options = [{'label': language_ind[x], 'value': x} for x in [0,1,2]],
                        value = 0,
                        style={'marginBottom': 10, "width":"100%"}
                    ),
                ),
                xs=5,
                sm=5,
                md=4,
                lg=3,
            ),
            justify="end",
        ),
    ]

def get_page_desc(id):
    return [
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Jumbotron(
                id=id,
                style={'paddingBottom':'0.5rem','paddingTop':'0.8rem'}
                )
            ]
            ),
        ],
        )
    ]
