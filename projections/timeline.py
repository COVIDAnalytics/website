import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import urllib
from projections.utils import get_cols, add_cases, get_df_projections, get_state_abbr
import pandas as pd


def get_bottom_visual():
    north_america_countries = ['Canada', 'Costa Rica', 'Cuba', 'Dominican Republic',
                               'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Panama',
                               'US']
    map_locations = ['US', "Europe", "Asia", "North America", "South America", "Africa", 'World']
    df_projections = get_df_projections()
    today = pd.Timestamp('today')
    df_projections = df_projections.loc[df_projections['Day'] >= today]
    data_csv_string = df_projections.to_csv(index=False, encoding='utf-8')
    data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)
    cols = get_cols()

    bottom_visual = [dbc.Row(
        no_gutters=True,
        children=[dbc.Col(
            xs=12,
            sm=12,
            md=6,
            lg=5,
            children=[dbc.Card(
                className="elevation-3 country-control-card",
                children=[dbc.CardBody(
                        style={"display": "flex", "alignItems": "flex-start", "width": "100%"},
                        children=[dbc.Col(
                            style={"padding": "0px"},
                            children=[
                                html.H6(
                                    "Which projections should be plotted?",
                                    style={
                                        "fontFamily": "Ubuntu",
                                        "color": "lightgrey",
                                        "fontSize": "20px",
                                    }
                                ),
                                html.Div(
                                    id="p2-transfer-dropdown-wrapper",
                                    children=dcc.Dropdown(
                                        className="flat-map-multi",
                                        id='predicted_timeline',
                                        options=[{'label': add_cases(x), 'value': x} for x in cols.keys()],
                                        value=['Total Detected'],
                                        clearable=False,
                                        multi=True,
                                    ),
                                ),
                            ]
                        ),
                    ]
                )]
            )]
        ),
        dbc.Col(
            xs=12,
            sm=12,
            md=6,
            lg=7,
            children=[dbc.Card(
                className="elevation-3 country-control-card",
                children=[dbc.CardBody([
                    html.H6(
                        id='province-card-title',
                        style={
                            "fontFamily": "Ubuntu",
                            "color": "lightgrey",
                            "paddingBottom": "6px",
                            "fontSize": "20px"
                        },
                    ),
                    dbc.Row(
                        style={"padding": "0 15px"},
                        children=[
                            dcc.Dropdown(
                                id='continent_dropdown',
                                className="loc-sel-drop loc-sel-slash no-left-padding",
                                options=[{'label': x, 'value': x} for x in map_locations],
                                clearable=False,
                                disabled=True,
                                placeholder="World"
                            ),
                            dcc.Dropdown(
                                id='country_dropdown',
                                className="loc-sel-drop loc-sel-slash",
                                placeholder="Country",
                                options=[{'label': x, 'value': x} for x in north_america_countries],
                            ),
                            dcc.Dropdown(
                                id='province_dropdown',
                                className="loc-sel-drop",
                                placeholder="State"
                            ),
                        ]
                    )
                ])],
            )],
        )],
    )]
    history_graph = [
        html.Div(
            id='state_projection_graph',
            className="elevation-3",
            children=[],
            style={
                'width': '100%',
            }
        ),
    ]

    return [html.Div(**{"data-aos": "fade-up", "data-aos-delay": "300"},
                     style={"zIndex": 2, "position": "relative"},
                     className="aos-refresh-onload-strict",
                     children=history_graph + bottom_visual)]
