import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from ventilators.utils import get_first_date, change2Percent

def get_transfers_visuals():
    df = pd.read_csv('data/predicted_ventilator/transfers_table-ihme.csv', sep=",", parse_dates = ['Date'])
    df.loc[:,'Date'] = pd.to_datetime(df['Date'], format='y%m%d').dt.date

    p1 = df.Param1.unique()
    p2 = df.Param2.unique()
    p3 = sorted(df.Param3.unique())
    min_date = min(df.Date.values)
    max_date = max(df.Date.values)

    del df

    firstDate = get_first_date()

    transfers_visuals = \
        [
            dbc.Row(
            [
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown("How much of its base supply is each state willing to share?"),
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Markdown("**Pooling Fraction:**")),
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id = 'p1-transfer-dropdown',
                                                        options = [{'label': change2Percent(x), 'value': x} for x in p1],
                                                        value = '0.1',
                                                    ),
                                                    id = "p1-transfer-dropdown-wrapper"
                                                ),
                                            ),
                                        ],
                                    ),
                                    dbc.Tooltip(
                                        "Example: for a pooling fraction of 10%, we guarantee that states will always keep at least 90% of their initial supply.",
                                        target="p1-transfer-dropdown-wrapper",
                                    ),
                                ],
                            ),
                        ],
                        className="h-100",
                    ),
                ],
                xs=12,
                sm=12,
                md=4,
                lg=4,
                ),
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown("How much additional safety supply would states like to have?"),
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Markdown("**Buffer:**")),
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id = 'p2-transfer-dropdown',
                                                        options = [{'label': change2Percent(x), 'value': x} for x in p2],
                                                        value = '0.2',
                                                    ),
                                                    id = "p2-transfer-dropdown-wrapper",
                                                ),
                                            ),
                                        ]
                                    ),
                                    dbc.Tooltip(
                                        "Example: for a buffer value of 20%, a projected demand of 1,000 ventilators implies a target supply of 1,200.",
                                        target="p2-transfer-dropdown-wrapper",
                                    ),
                                ],
                            ),
                        ],
                        className="h-100",
                    ),
                ],
                xs=12,
                sm=12,
                md=4,
                lg=4,
                ),
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown("How much would you like to adjust the federal surge supply?"),
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Markdown("**Surge Supply:**")),
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id = 'p3-transfer-dropdown',
                                                        options = [{'label': change2Percent(x), 'value': x} for x in p3],
                                                        value = '0.75',
                                                    ),
                                                    id = "p3-transfer-dropdown-wrapper",
                                                ),
                                            ),
                                        ]
                                    ),
                                    dbc.Tooltip(
                                        "Example: a value of 50% adjusts the baseline estimate of 450 ventilators per day to 225 ventilators per day.",
                                        target="p3-transfer-dropdown-wrapper",
                                    ),
                                ],
                            ),
                        ],
                        className="h-100",
                    ),
                ],
                xs=12,
                sm=12,
                md=4,
                lg=4,
                ),
            ],
            ),
        ] + \
        [
            dbc.Row(
                [
                    dbc.Col(
                    [
                        dbc.Alert("By optimizing ventilator allocation across states, we can quickly eliminate the shortage of ventilators in every state.",
                                  color="primary"),
                    ],
                    style={"marginTop": "1rem"},
                    )
                ]
            )
        ] + \
        [
            dbc.Row(
            [
                dbc.Col(
                [
                    html.Div(
                        id = 'us_transfers_graph',
                        children = [],
                    ),
                ],
                xs=12,
                sm=12,
                md=6,
                lg=6,
                ),
                dbc.Col(
                [
                    html.Div(
                        id = 'us_map_transfers_vent',
                        children = [],
                    ),
                    html.H6('Date:',id="date-projections"),
                    html.Div(
                        dcc.DatePickerSingle(
                            id='date-transfer-dropdown',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            date=firstDate,
                            initial_visible_month=firstDate,
                            style={'marginBottom':20}
                        ),
                        id="date-projections-picker-div"
                    ),
                ],
                xs=12,
                sm=12,
                md=6,
                lg=6,
                ),
            ]
            ),
        ]
    return transfers_visuals
