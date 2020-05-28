import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

from navbar import Navbar
from footer import Footer

from ventilators.shortage import get_shortage
from ventilators.transfers_visuals import get_transfers_visuals
from ventilators.transfers_table import get_transfers_table

def VentilatorAllocations():

    nav = Navbar()
    footer = Footer()

    models = ["Washington IHME","COVIDAnalytics"]

    body = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Jumbotron(
                        [
                            html.H1("Optimization can solve the ventilator shortage"),
                            html.P('''
                                   For severe COVID-19 patients, medical ventilators can spell \
                                   the difference between life and death, but many locations are \
                                   already experiencing shortages.
                                   ''',
                                   className="lead"),
                            html.Hr(),
                            dcc.Markdown('''Fortunately, the dynamics of the \
                                         pandemic differ from one place to another, \
                                         creating opportunities to mitigate shortages by \
                                         dynamically allocating the global ventilator supply.'''),
                        ],
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Between hospitals"),
                                               style={"textAlign": "center"}),
                                dbc.CardImg(src="assets/collaborators/photos/Hartford_logo.jpg",
                                            top=False,
                                            style={"paddingLeft":   "10px",
                                                   "paddingRight":  "10px",
                                                   "paddingBottom": "40px",
                                                   "paddingTop":    "40px",}),
                                dbc.CardFooter(
                                    [
                                        html.P("We are working with our partners at Hartford \
                                               HealthCare to ensure that ventilator demand is met \
                                               across hospitals in their network."),
                                    ],
                                    className="h-100",
                                )
                            ],
                            style={"borderColor": "#800020"},
                            className="h-100"
                        ),
                        xs=12,
                        sm=6,
                        md=6,
                        lg=4,
                        xl=4,
                        style={"padding": "20px"},
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Between states"),
                                               style={"textAlign": "center"}),
                                dbc.CardImg(src="assets/images/allocation.png", top=False),
                                dbc.CardFooter(
                                    [
                                        html.P("We show below how ventilator pooling \
                                               across \
                                               states can solve the US shortage, even without \
                                               federal intervention."),
                                    ],
                                    className="h-100",
                                ),
                            ],
                            style={"borderColor": "#800020"},
                            className="h-100",
                        ),
                        xs=12,
                        sm=6,
                        md=6,
                        lg=4,
                        xl=4,
                        style={"padding": "20px"},
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Between countries"),
                                               style={"textAlign": "center"}),
                                dbc.CardImg(src="assets/images/world-map.png", top=False,
                                            style={"paddingLeft":   "10px",
                                                   "paddingRight":  "10px",
                                                   "paddingBottom": "20px",
                                                   "paddingTop":    "20px",}),
                                dbc.CardFooter(
                                    [
                                        html.P("We hope our optimization model will provide a \
                                               blueprint for international collaboration on \
                                               ventilator inventory management.")
                                    ],
                                    className="h-100",
                                )
                            ],
                            style={"borderColor": "#800020"},
                            className="h-100",
                        ),
                        xs=12,
                        sm=6,
                        md=6,
                        lg=4,
                        xl=4,
                        style={"padding": "20px"},
                    ),
                ],
                justify="around",
            ),
            dbc.Row(
                [
                    html.Iframe(src="https://www.youtube.com/embed/SwiOFEZc0Gs",
                                width="711",
                                height="400"),
                ],
                justify="around",
                style={"paddingBottom": "20px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Markdown('''Interested in more details? Check out this \
                                         [technical report](/ventilator_documentation_pdf), \
                                         or take a look at our [code]\
                                         (https://github.com/COVIDAnalytics/ventilator-allocation)!
                                         '''),
                        ],
                    ),
                ],
            ),
            dbc.Row(
            [
                dbc.Jumbotron(
                [
                    html.H2("Why share ventilators between states?"),
                    html.P('''As highlighted in the visuals below, the number of ventilators \
                              available across all 50 states - without even accounting for the \
                              federal stockpile - exceeds national demand.''',
                           className="lead"),
                    html.Hr(),
                    dcc.Markdown('''Yet with the current \
                                 allocation of ventilators, some states are expected to face strong \
                                 shortages over time. And this is true for different pandemic \
                                 projection models, including our own [DELPHI](/projections) \
                                 forecasts and those from the [University of Washington’s IHME model]\
                                 (https://covid19.healthdata.org/united-states-of-america).
                                 '''),
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
                    html.H6('Select the Data Source:',id="date-projections"),
                    html.Div(
                        dcc.Dropdown(
                            id = 'base-model-dropdown',
                            options = [{'label': x, 'value': x} for x in models],
                            value = 'COVIDAnalytics',
                        ),
                    ),
                ],
                ),
            ]
            )
        ] + \
            get_shortage() + \
        [
            dbc.Row(
                [
                    dbc.Jumbotron(
                    [
                        html.H2("How can states share ventilators optimally?"),
                        dcc.Markdown('''
                            We know how many ventilators are in each state from public data, and we \
                            estimate that up to 450 ventilators per day could be made available \
                            through a federal surge \
                            (see [documentation](/ventilator_documentation_pdf) for details). \
                            Our optimization model recommends surge supply allocations and interstate transfers to reduce ventilator shortage as quickly and efficiently as possible.'''),
                        html.Hr(),
                        html.P('Use the interactive tool below to experiment with different reallocation policies.', className="lead"),
                    ]
                    ),
                ],
            )
        ] + \
            get_transfers_visuals() + \
            get_transfers_table() + \
        [
            dbc.Row([
        			dbc.Col(
        				html.Div(
        					html.A(
        						"Download the Ventilator Shortage Data",
        						id="download-link-demand",
                                download="covid_analytics_ventilator_demand.csv",
        	        			target="_blank"
        					),
        					style={'textAlign':"center"}
        				)
        			),
        			dbc.Col(
        				html.Div(
        					html.A(
        						"Download the Ventilator Transfers Data",
        						id="download-link-tranfers",
                                download="covid_analytics_ventilator_transfers.csv",
        	        			target="_blank"
        					),
        					style={'textAlign':"center"}
        				)
        			),
        		]
            ),
        ],
       className="page-body"
    )

    layout = html.Div([nav, body, footer],className="site")
    return layout
