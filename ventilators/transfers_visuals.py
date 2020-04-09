import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from ventilators.utils import df_mod1_transfers, oneWeekFromNow, state_cols
from ventilators.utils import model_visual, models, change2Percent

transfers_visuals = \
    [
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Date:',id="date-projections"),
                html.Div(
                    dcc.DatePickerSingle(
                        id='date-transfer-dropdown',
                        min_date_allowed=min(df_mod1_transfers.Date.values),
                        max_date_allowed=max(df_mod1_transfers.Date.values),
                        date=oneWeekFromNow,
                        initial_visible_month=oneWeekFromNow,
                        style={'marginBottom':20}
                    ),
                    id="date-projections-picker-div"
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Pooling Fraction:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'p1-transfer-dropdown',
                        options = [{'label': change2Percent(x), 'value': x} for x in df_mod1_transfers.Param1.unique()],
                        value = '0.1',
                    ),
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Buffer:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'p2-transfer-dropdown',
                        options = [{'label': change2Percent(x), 'value': x} for x in df_mod1_transfers.Param2.unique()],
                        value = '0.2',
                    ),
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Surge Supply:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'p3-transfer-dropdown',
                        options = [{'label': change2Percent(x), 'value': x} for x in df_mod1_transfers.Param3.unique()],
                        value = '0.75',
                    ),
                ),
            ]
            ),
        ],
        ),
    ] + \
    [
        dbc.Row(
            [
                dbc.Col(
                [
                    html.H6("By intelligent optimization via the ventilator allocation \
                    model, we are able to reduce the shortage of ventilators in the states \
                    substantially.",id="graph-vent-text"),
                ]
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
            ],
            xs=12,
            sm=12,
            md=6,
            lg=6,
            ),
        ]
        ),
    ]
