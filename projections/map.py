import datetime
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from projections.utils import get_cols, build_card, add_cases

def get_top_visual():
    map_locations = ['US', "Europe", "Asia", "North America", "South America", "Africa", 'World']
    cols = get_cols()
    today = pd.Timestamp('today')
    oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)
    df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates = ['Day'])
    df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
    df_projections = df_projections.loc[df_projections['Day']>=today]

    top_visual = [
            dbc.Row(
            [
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown("For what date do you want to see projections?"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    dcc.DatePickerSingle(
                                                        id='us-map-date-picker-range',
                                                        min_date_allowed=today,
                                                        max_date_allowed=max(df_projections.Day.values),
                                                        date=oneWeekFromNow,
                                                        initial_visible_month=oneWeekFromNow,
                                                    ),
                                                    id="date-projections-picker-div"
                                                ),
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
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown("And for which area?"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                    dcc.Dropdown(
                                                            id = 'location_map_dropdown',
                                                            options = [{'label': x, 'value': x} for x in map_locations],
                                                            value = 'US',
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
            style={'marginBottom':20,'marginTop':20},
            )
        ] + \
        [
            dbc.Row(
            [
                html.Div(
                    id='us-stats-title',
                    style={
                        'width': '100%',
                        'color': 'black',
                        'textAlign': 'center',
                        'fontSize': 30,
                        'fontWeight':'bold'
                        }
                ),
            ],
            )
        ] + \
        [
            dbc.Row(
            [
                build_card('us_tot_det'),
                build_card('us_tot_death'),
                build_card('us_active'),
                build_card('us_active_hosp')
            ],
            align="center"
            )
        ] + \
        [
            dbc.Row(
            [
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown('Predicted Value:'),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id = 'us_map_dropdown',
                                                        options = [{'label': add_cases(x), 'value': x} for x in cols.keys()],
                                                        value = 'Total Detected',
                                                    ),

                                                    id="predicted-value-projections-picker-div",
                                                ),
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
                dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    dcc.Markdown("And for which population type?"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                    dcc.RadioItems(
                                                    options=[
                                                        {'label': '  Full population', 'value': 1},
                                                        {'label': '  Value per million', 'value': 2}
                                                    ],
                                                    value=1,
                                                    id = 'radio_botton',
                                                    labelStyle={'display': 'inline-block',
                                                    'margin-right': '20px'
                                                                   },
                                                    style={'textAlign': 'center'}
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
            style={'marginBottom':20,'marginTop':20},
            )
        ]  + \
        [
            dbc.Row(
            [
                dbc.Col(
                [
                    html.Div(
                        id = 'map_projections',
                        children = [],
                    ),
                    html.P(
                            children = [],
                            style={'color':'gray'},
                            id='grey-countries-text'
                    ),
                ]
                ),

            ],
            )
        ]
    return top_visual
