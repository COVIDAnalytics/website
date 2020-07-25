import datetime
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from projections.utils import get_cols, add_cases

def build_card_content(num, title):
    return [html.Div(
        className="statCard statSubCard",
        children=[
            html.Div(
                style={"padding": "15px"},
                children=[
                    html.H4(title),
                    html.H3(num),
                ]
            )
        ])
    ]

def build_card(_id, c):
    return dbc.Col(
        id=_id,
        xs=12,
        sm=6,
        md=6,
        lg=6,
        className=c,
        style={},
    )


def build_death_cards():
    today = pd.Timestamp('today')
    oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)
    map_locations = ['US', "Europe", "Asia", "North America", "South America", "Africa", 'World']
    df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates = ['Day'])
    df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
    df_projections = df_projections.loc[df_projections['Day']>=today]
    return [
        dbc.Row([
            html.Div(
                id='us-stats-title',
                style={
                    'display': 'none',
                    'width': '100%',
                    'color': 'black',
                    'textAlign': 'center',
                    'fontSize': 30,
                    'fontWeight': 'bold'
                }
            ),
        ]),
        dbc.Row(
            align="center",
            no_gutters=True,
            className="elevation-3",
            style={"padding": "0px"},
            children=[
                build_card('us_tot_det', "tl"),
                build_card('us_tot_death', "tr"),
                build_card('us_active', "bl"),
                build_card('us_active_hosp', "br"),
                dbc.Col(
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                    className="statConfig",
                    children=[
                        html.Div(
                            className="statCard statSubCard",
                            children=[
                                dbc.Row(
                                    align="stretch",
                                    justify="center",
                                    no_gutters=True,
                                    style={"position": "relative", "zIndex": 20},
                                    children=[
                                    dcc.DatePickerSingle(
                                        id='us-map-date-picker-range',
                                        className="flat-date-picker",
                                        placeholder="04/04/2020",
                                        min_date_allowed=today,
                                        max_date_allowed=max(df_projections.Day.values),
                                        date = oneWeekFromNow,
                                        initial_visible_month = oneWeekFromNow,
                                    ),
                                    html.Div(className="buffer", style={"width": "55px"}),
                                    dcc.Dropdown(
                                        id='location_map_dropdown',
                                        className="flat-location-picker",
                                        options=[{'label': x, 'value': x} for x in map_locations],
                                        value='US',
                                        clearable=False,

                                    ),
                                ])
                            ]
                        )
                    ]
                )
            ],
        )
    ]

def get_top_visual():
    cols = get_cols()
    today = pd.Timestamp('today')
    df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates = ['Day'])
    df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date

    map_controls = [dbc.Row(
        no_gutters=True,
        style={'marginBottom': 20},
        children=[dbc.Col(
            xs=12,
            sm=12,
            md=6,
            lg=6,
            children=[
                dbc.Card(
                    className="country-control-card elevation-3",
                    children=[
                        dbc.CardBody([
                            #dcc.Markdown('Predicted Value:'),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        id="predicted-value-projections-picker-div",
                                        children=dcc.Dropdown(
                                            className="flat-location-picker flat-map-drop",
                                            clearable=False,
                                            id = 'us_map_dropdown',
                                            options = [{'label': add_cases(x), 'value': x} for x in cols.keys()],
                                            value = 'Total Detected',
                                        ),
                                    ),
                                ),
                            ]),
                        ]),
                    ],
                ),
            ],
        ),
        dbc.Col(
            xs=12,
            sm=12,
            md=6,
            lg=6,
            children=[dbc.Card(
                className="country-control-card elevation-3",
                children=[dbc.CardBody([
                    dcc.Markdown("And for which population type?"),
                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                dcc.RadioItems(
                                    options=[
                                        {'label': '  Full population', 'value': 1},
                                        {'label': '  Value per million', 'value': 2}
                                    ],
                                    value=1,
                                    id = 'radio_botton',
                                    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                                    style={'textAlign': 'center'}
                                ),
                            ]),
                        ),
                    ]),
                ])],
            )]
        ),
        html.P(
            children=[],
            style={'color': 'gray'},
            id='grey-countries-text'
        ),
    ])]
    map_graph = [
            dbc.Row(
            [
                dbc.Col(
                [
                    html.Div(
                        id='map_projections',
                        className="elevation-3",
                        style={"padding": "20px"},
                        children = [],
                    ),

                ]
                ),

            ],
            )
        ]
    return map_graph + map_controls
