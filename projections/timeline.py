import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from projections.utils import df_projections, cols, data_csv_string

bottom_visual = \
    [
        dbc.Row(
            [
                dbc.Col(
                [
                    html.H5('Use the tool below to explore our predictions for different locations.'),
                ]
                ),
            ],
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
                                dcc.Markdown("What value would you like to plot?"),
                                dbc.Row(
                                    [
                                        dbc.Col(dcc.Markdown("**Predicted  \n Value:**"),width="auto"),
                                        dbc.Col(
                                            html.Div(
                                                dcc.Dropdown(
                                                    id = 'predicted_timeline',
                                                    options = [{'label': x, 'value': x} for x in cols.keys()],
                                                    value = ['Active'],
                                                    multi=True,
                                                ),
                                                id = "p2-transfer-dropdown-wrapper",
                                            ),
                                        width=True
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                    className="h-100",
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
                                dcc.Markdown("For what location in the previously chosen area?"),
                                dbc.Row(
                                    [
                                        dbc.Col([dcc.Markdown("**Country:**"),dcc.Markdown("**Province / State:**")]),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                dcc.Dropdown(
                                                        id = 'country_dropdown',
                                                        options = [{'label': x, 'value': x} for x in df_projections[df_projections['Continent'] == 'North America']['Country'].drop_duplicates()],
                                                        #value = 'US',
                                                ),

                                                dcc.Dropdown(
                                                        id = 'province_dropdown',
                                                ),
                                                #html.Hr(),

                                                html.Div(id = "p2-transfer-dropdown-wrapper"),

                                            ]),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                    className="h-100",
                ),
            ],
            xs=12,
            sm=12,
            md=6,
            lg=6,
            ),
        ],
        )
    ] + \
    [
         dbc.Row(
         [
               dbc.Col(
               [
                     html.Div(
                         id = 'state_projection_graph',
                         children = [],
                         style={
                             'width': '100%',
                             'display': 'inline-block',
                             'paddingTop': 20,
                             }
                     ),
                ]
                )
          ],
          )
    ] + \
    [
         dbc.Row([
            dbc.Col(
                html.Div(
                    html.A(
                        "Download the Data",
                        id="download-link",
                        download="covid_analytics_projections.csv",
                        href=data_csv_string,
                        target="_blank"
                    ),
                    style={'textAlign':"center"}
                )
            ),
            ]
        ),
    ]
