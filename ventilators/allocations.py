import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

from navbar import Navbar
from footer import Footer
from assets.mappings import states, colors
from ventilators.shortage import shortage
from ventilators.utils import df_mod1_shortages, df_mod1_transfers, df_mod1_projections
from ventilators.utils import df_mod2_shortages, df_mod2_transfers, df_mod2_projections
from ventilators.utils import df_mod1_transfers, oneWeekFromNow, state_cols
from ventilators.utils import no_model_visual, model_visual, models, change2Percent

nav = Navbar()
footer = Footer()

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                html.H2("Ventilator Allocation"),
                html.P("""\
                        For severe COVID-19 patients, medical ventilators can spell the\
                         difference between life and death. These devices are increasingly\
                          in demand, with some US states already experiencing shortages. \
                          Fortunately, the dynamics of the pandemic differ from one state to \
                          another, creating opportunities to mitigate shortages by pooling some of \
                          the ventilator supply across states. We propose an optimization model to \
                          design ventilator pooling strategies and support health care providers and\
                           policymakers in their resource allocation decisions.
                       """),
                dcc.Markdown('''For more details on the optimization model, we refer the user to the\
                 [documentation](/ventilators_documentation).'''),
                dcc.Markdown('''**Need for ventilator pooling**'''),
                dcc.Markdown('''We first illustrate why ventilator pooling can alleviate shortages \
                in the United States. The graph below shows that the number of ventilators available \
                across all 50 states---without accounting for the federal stockpile---can be sufficient \
                to satisfy overall demand. Yet, the map shows that, with the current allocation of \
                ventilators, some states are expected to face strong shortages over time. \
                When exploring these visuals, you can choose between two different pandemic \
                prediction models: the [University of Washington’s IHME model]\
                (https://covid19.healthdata.org/united-states-of-america) and [our SEIR epidemiological model]\
                (/projections).'''),
            ]
            ),
        ],
        ),
        shortage,
        dbc.Row(
            [
                dbc.Col(
                [
                    dcc.Markdown('''**Ventilator pooling results**'''),
                    dcc.Markdown('''We now propose an interactive tool which allows the user \
                    to experiment with different reallocation policies and see the resulting \
                    impact on shortfalls. '''),
                    dcc.Markdown('''You can choose:'''),
                    dcc.Markdown('''
                      1. Data Source: Which pandemic prediction models to use to estimate ventilator demand.
                      2. Pooling Fraction: Fraction of each state’s initial ventilator supply that is \
                      available for sharing with other states. For instance, if the Pooling Fraction \
                      is 10%, the model guarantees that each state will retain at least 90% of its \
                      initial supply.
                      3. Buffer: Percentage of additional demand that states would like to plan for \
                      (with buffer supply of ventilators). For instance, if the Buffer is 10% and \
                      the demand in a given state on a given day is 40,000 ventilators, then the \
                      state would ideally like to get 44,000 ventilators. **We place a (smaller) \
                      penalty on unmet demand in this range.**
                      4. Surge Supply Availability: Scaling factor to adjust the available surge \
                      supply of ventilators from the federal government. Our baseline estimate of \
                      surge supply is 450 ventilators per day for the next 30 days. \
                      To cope with uncertainty in this estimate, we let the user vary this number.
                    '''),
                    dcc.Markdown('''You will find additional data sources and parameter choices on our \
                    [documentation](/ventilators_documentation).'''),
                ]
                ),
            ],
            ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Base Model:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'base-model-dropdown_transfers',
                        options = [{'label': x, 'value': x} for x in models],
                        value = 'Washington IHME',
                    ),
                ),
            ],
            ),
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
                        style={'margin-bottom':20}
                    ),
                    id="date-projections-picker-div"
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Value Calculated:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'val-transfer-dropdown',
                        options = [{'label': model_visual[x], 'value': x} for x in state_cols],
                        value = 'Demand',
                    ),
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
                html.H6('Surge Supply Availability:',id="date-projections"),
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
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                    id = 'us_map_transfers_vent',
                    children = [],
                ),
            ]
            ),
            dbc.Col(
            [
                html.Div(
                    id = 'us_transfers_graph',
                    children = [],
                ),
            ]
            ),
        ]
        ),
        dbc.Row(
            [
                dbc.Col(
                [
                    html.H6('Transfer:',id="date-projections"),
                ]
                ),
                dbc.Col(
                [
                    html.Div(
                        dcc.Dropdown(
                            id = 'transfer-to-from-dropdown',
                            options = [{'label': x, 'value': x} for x in ["to", "from"]],
                            value = 'to',
                        ),
                    ),
                ]
                ),
                dbc.Col(
                [
                    html.Div(
                        dcc.Dropdown(
                            id = 'transfer-state-dropdown',
                            options = [{'label': x, 'value': x} for x in models],
                            value = '',
                        ),
                        style={'text-align':"center"}
                    ),
                ]
                ),
            ],
            ),
            dbc.Row([
                dbc.Col(
                [
                    html.Div(id='table-text',children='',style={'padding-top':"20px"}),
                ]
                ),
            ],
            ),
            dbc.Row([
                dbc.Col(
                [
                    dash_table.DataTable(
                            id="transfer_list",
                            columns=[{'id': c, 'name': c} for c in ["State","Units"]],
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                            },
                            style_table={
                                'overflow':'visible',
                                'maxHeight': '300px',
                                'maxWidth': '500px',
                                'border': 'thin lightgrey solid',
                            },
                            style_cell={
                                'height': 'auto',
                                'minWidth': '0px',
                                'width': '50px',
                                'maxWidth': '180px',
                                'whiteSpace': 'normal',
                                'textAlign': 'center',
                                'font_size': '14px',
                                'font-family': 'arial',
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ],
                            style_header={
                                'display': 'none',
                            }
                        )
                ],
                ),
            ],
            ),
        dbc.Row([
                dbc.Col(
                [
                    html.H6('Select Model - Download Data:',id="date-projections"),
                    html.Div(
                        dcc.Dropdown(
                            id = 'base-model-dropdown_download',
                            options = [{'label': x, 'value': x} for x in models],
                            value = 'Washington IHME',
                        ),
                    ),
                ],
                ),
    		],
            align="center",
            ),
        dbc.Row([
    			dbc.Col(
    				html.Div(
    					html.A(
    						"Download the Ventilator Shortage Data",
    						id="download-link-demand",
    						download="covid_analytics_ventilator_demand.csv",
    	        			target="_blank"
    					),
    					style={'text-align':"center"}
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
    					style={'text-align':"center"}
    				)
    			),
    		]
        ),
    ],
   className="page-body"
)

def VentilatorAllocations():
    layout = html.Div([nav, body, footer],className="site")
    return layout
