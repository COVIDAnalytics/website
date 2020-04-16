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
                html.H2("Optimization can solve the ventilator shortage"),
                dcc.Markdown('''\
                        For severe COVID-19 patients, medical ventilators can spell the\
                         difference between life and death. These devices are increasingly\
                          in demand, with some US states already experiencing shortages. \
                          Fortunately, the dynamics of the pandemic differ from one state to \
                          another, creating opportunities to mitigate shortages by pooling some of \
                          the ventilator supply across states. Details on data and models can be found in the\
                 [technical report](/ventilator_documentation_pdf), and our source code is available on [GitHub](https://github.com/COVIDAnalytics/ventilator-allocation).'''),
                html.H4("Why share ventilators between states?"),
                dcc.Markdown('''As highlighted in the visuals below, the number of ventilators available \
                across all 50 states - without even accounting for the federal stockpile - exceeds national demand. Yet with the current allocation of \
                ventilators, some states are expected to face strong shortages over time. \
                And this is true for different pandemic projection models, including [our own forecasts](/projections) and those of the [University of Washington’s IHME model]\
                (https://covid19.healthdata.org/united-states-of-america).'''),
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
        shortage + \
    [
        dbc.Row(
            [
                dbc.Col(
                [
                    html.H4("How can states share ventilators optimally?"),
                    dcc.Markdown('''
                        We know how many ventilators are in each state from public data, and we \
                        estimate that up to 450 ventilators per day could be made available \
                        through a federal surge \
                        (see [documentation](/ventilator_allocation_documentation) for details). \
                        Our optimization model recommends surge supply allocations and interstate transfers to reduce ventilator shortage as quickly and efficiently as possible.'''),
                    html.H5('Use the interactive tool below to experiment with different reallocation policies.'),
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
