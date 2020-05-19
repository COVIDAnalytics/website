import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from ventilators.utils import get_first_date, get_no_model_visual, get_df_mod1_projections

def get_shortage():
    firstDate = get_first_date()
    _ , params = get_df_mod1_projections(True)
    state_cols = ["Shortage","Supply","Demand"]
    no_model_visual = get_no_model_visual()
    # Defines the top of the page, where the current situation is displayed (no optimization yet)
    shortage = \
        [dbc.Row(
            [
                dbc.Col(
                [
                    dbc.Alert("The total ventilator supply in the US exceeds projected demand, \
                    but imbalanced demand from local 'hot spots' leads to shortages.", color="danger"),
                ]
                )
            ]
        )] + \
        [dbc.Row(
            [
                dbc.Col(
                [
                    html.Div(
                        id = 'us_ventilator_graph',
                        children = [],
                        style={
                            'width': '100%',
                            'display': 'inline-block',
                            }
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
                        id = 'us_map_projections_vent',
                        children = [],
                        style={
                            'width': '100%',
                            'display': 'inline-block',
                            }
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                            [
                                html.H6('Date:',id="date-projections"),
                                html.Div(
                                    dcc.DatePickerSingle(
                                        id='us-map-date-picker-range-vent',
                                        min_date_allowed=params[0],
                                        max_date_allowed=params[1],
                                        date=firstDate,
                                        initial_visible_month=firstDate,
                                        style={'marginBottom':20}
                                    ),
                                    id="date-projections-picker-div"
                                ),
                            ],
                            xs=12,
                            sm=4,
                            md='auto',
                            lg='auto',
                            ),
                            dbc.Col(
                            [
                                html.H6('Plotted Value:',id="date-projections"),
                                html.Div(
                                    dcc.Dropdown(
                                        id = 'us_map_dropdown-vent',
                                        options = [{'label': no_model_visual[x], 'value': x} for x in state_cols],
                                        value = 'Shortage',
                                        style={'marginBottom':20}
                                    ),
                                ),
                            ],
                            xs=12,
                            sm=8,
                            md=True,
                            lg=True,
                            )
                        ]
                    ),
                ],
                xs=12,
                sm=12,
                md=6,
                lg=6,
                ),
            ]
        )
    ]
    return shortage
