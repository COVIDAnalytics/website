### Data
import pandas as pd
import datetime
import urllib
### Graphing
import plotly.graph_objects as go
import plotly.express as px
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer
from assets.mappings import states, colors

nav = Navbar()
footer = Footer()


df_vent_state = pd.read_csv('data/predicted_ventilator/state_supplies_table-ihme.csv', sep=",", parse_dates = ['Date'])
df_vent_transfers = pd.read_csv('data/predicted_ventilator/transfers_table-ihme.csv', sep=",", parse_dates = ['Date'])

today = pd.Timestamp('today')
oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)
df_projections.loc[:,'Date'] = pd.to_datetime(df_projections['Date'], format='y%m%d').dt.date
df_projections = df_projections.loc[df_projections['Date']>=today]

state_cols = []
transfers_cols = []
models = ["model1","model2"]


dataset_state = "data/predicted/Allstates.csv"
state_csv_string = df_projections.to_csv(index=False, encoding='utf-8')
state_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(state_csv_string)

dataset_transfers = "data/predicted/Allstates.csv"
transfers_csv_string = dataset_transfers.to_csv(index=False, encoding='utf-8')
transfers_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(transfers_csv_string)


body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                html.H2("Ventilator Allocation"),
                html.P("""\
                        blah blah
                       """),
                dcc.Markdown('''You can read more about the model [here](/ventilators_documentation).'''),
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
                        id = 'base-model-dropdown',
                        options = [{'label': x, 'value': x} for x in models],
                        value = 'model1',
                    ),
                ),
            ],
            ),
        ]
    ],
   className="page-body"
)

def VentilatorAllocations():
    layout = html.Div([nav, body, footer],className="site")
    return layout
