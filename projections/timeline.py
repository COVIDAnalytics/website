import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import urllib
from projections.utils import get_cols, add_cases, get_df_projections


def get_bottom_visual():
    north_america_countries = ['Canada', 'Costa Rica', 'Cuba', 'Dominican Republic',
                               'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Panama',
                               'US']
    df_projections = get_df_projections()
    data_csv_string = df_projections.to_csv(index=False, encoding='utf-8')
    data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)
    cols = get_cols()

    explanation = [dbc.Row([
        dbc.Col([
            html.H5('Use the tool below to explore our predictions for different locations.'),
        ]),
    ])]
    bottom_visual = [dbc.Row(
        style={'marginBottom': 20, 'marginTop': 20},
        children=[dbc.Col(
            xs=12,
            sm=12,
            md=6,
            lg=6,
            children=[dbc.Card(
                className="projections-general-card h-100",
                children=[dbc.CardBody([
                    dcc.Markdown("What value would you like to plot?"),
                    dbc.Row([
                        dbc.Col(dcc.Markdown("**Predicted  \n Value:**"), width="auto"),
                        dbc.Col(
                            html.Div(
                                id="p2-transfer-dropdown-wrapper",
                                children=dcc.Dropdown(
                                    id='predicted_timeline',
                                    options=[{'label': add_cases(x), 'value': x} for x in cols.keys()],
                                    value=['Total Detected'],
                                    multi=True,
                                ),
                            ),
                            width=True
                        ),
                    ]),
                ])],
            )]
        ),
            dbc.Col(
                xs=12,
                sm=12,
                md=6,
                lg=6,
                children=[dbc.Card(
                    className="projections-general-card h-100",
                    children=[dbc.CardBody([
                        html.Div(
                            id='province-card-title',
                            style={'paddingBottom': 10}
                        ),
                        dbc.Row([
                            dbc.Col([dcc.Markdown("**Country:**"), dcc.Markdown("**Province / State:**")]),
                            dbc.Col(
                                html.Div([
                                    dcc.Dropdown(
                                        id='country_dropdown',
                                        options=[{'label': x, 'value': x} for x in north_america_countries],
                                    ),
                                    dcc.Dropdown(
                                        id='province_dropdown',
                                    ),
                                    html.Div(id="p2-transfer-dropdown-wrapper"),
                                ]),
                            ),
                        ])
                    ])],
                )],
            )],
    )]
    history_graph = [dbc.Row([
        dbc.Col([
            html.Div(
                id='state_projection_graph',
                className="elevation-3",
                children=[],
                style={
                    'width': '100%',
                    'display': 'inline-block',
                    'padding': 20,
                    'marginTop': "30px"
                }
            ),
        ])
    ])]
    pre_footer = [dbc.Row([
        dbc.Col(
            html.Div(
                style={'textAlign': "center"},
                children=html.A(
                    "Download Most Recent Predictions",
                    id="download-link",
                    download="covid_analytics_projections.csv",
                    href=data_csv_string,
                    target="_blank"
                ),
            )
        ),
    ])]
    return history_graph + bottom_visual + pre_footer
