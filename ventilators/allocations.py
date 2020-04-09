import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

from navbar import Navbar
from footer import Footer
from assets.mappings import states, colors
from ventilators.shortage import shortage
from ventilators.transfers_visuals import transfers_visuals
from ventilators.transfers_table import transfers_table
from ventilators.utils import df_mod1_shortages, df_mod1_transfers, df_mod1_projections
from ventilators.utils import df_mod2_shortages, df_mod2_transfers, df_mod2_projections
from ventilators.utils import oneWeekFromNow, state_cols
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
                dcc.Markdown('''For more details on the optimization model and the data that we utilize, we refer the user to the\
                 [documentation](/ventilators_documentation).'''),
                dcc.Markdown('''**Why share ventilators between states?**'''),
                dcc.Markdown('''The graph below shows that the number of ventilators available \
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
                        value = 'Washington IHME',
                    ),
                ),
            ],
            ),
        ]
        )
    ] + \
        shortage + \
    [
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
                      1. **Data Source**: Which pandemic prediction models to use to estimate ventilator demand.
                      2. **Pooling Fraction**: Fraction of each state’s initial ventilator supply that is \
                      available for sharing with other states. For instance, if the Pooling Fraction \
                      is 10%, the model guarantees that each state will retain at least 90% of its \
                      initial supply.
                      3. **Buffer**: Percentage of additional demand that states would like to plan for \
                      (with buffer supply of ventilators). For instance, if the Buffer is 10% and \
                      the demand in a given state on a given day is 1,000 ventilators, then the \
                      state would ideally like to have a stock of 1,100 ventilators.
                      4. **Surge Supply Availability**: Scaling factor to adjust the available surge \
                      supply of ventilators from the federal government. Our baseline estimate of the \
                      federal stockpile available is 13,500 and is available for a release to the states in the next 30 days, i.e., \
                      450 ventilators per day. \
                      To cope with uncertainty in this estimate, we let the user vary this number.
                    '''),
                    dcc.Markdown('''You will find additional data sources and parameter choices on our \
                    [documentation](/ventilators_documentation).'''),
                ]
                ),
            ],
        )
    ] + \
        transfers_visuals + \
        transfers_table + \
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

def VentilatorAllocations():
    layout = html.Div([nav, body, footer],className="site")
    return layout
