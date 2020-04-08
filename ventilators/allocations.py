### Data
import pandas as pd
import datetime
import urllib
### Graphing
import plotly.graph_objects as go
import plotly.express as px
### Dash
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer
from assets.mappings import states, colors

nav = Navbar()
footer = Footer()


df_vent_state_mod1 = pd.read_csv('data/predicted_ventilator/state_supplies_table-ihme.csv', sep=",", parse_dates = ['Date'])
df_vent_transfers_mod1 = pd.read_csv('data/predicted_ventilator/transfers_table-ihme.csv', sep=",", parse_dates = ['Date'])

df_vent_state_mod2 = pd.read_csv('data/predicted_ventilator/state_supplies_table-ihme.csv', sep=",", parse_dates = ['Date'])
df_vent_transfers_mod2 = pd.read_csv('data/predicted_ventilator/transfers_table-ihme.csv', sep=",", parse_dates = ['Date'])

today = pd.Timestamp('today')
oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)

df_vent_state_mod1.loc[:,'Date'] = pd.to_datetime(df_vent_state_mod1['Date'], format='y%m%d').dt.date
df_vent_state_mod1 = df_vent_state_mod1.loc[df_vent_state_mod1['Date']>=today]
df_vent_state_mod2.loc[:,'Date'] = pd.to_datetime(df_vent_state_mod2['Date'], format='y%m%d').dt.date
df_vent_state_mod2 = df_vent_state_mod2.loc[df_vent_state_mod1['Date']>=today]

state_cols = ["Supply_Excess","Supply","Demand"]
transfers_cols = []
models = ["Washington IHME","COVIDAnalytics"]

def change2Percent(frac):
    return str(100*(1-frac))+'%'

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
                        value = 'Washington IHME',
                    ),
                ),
            ],
            ),
        ]
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Date:',id="date-projections"),
                html.Div(
                    dcc.DatePickerSingle(
                        id='us-map-date-picker-range-vent',
                        min_date_allowed=min(df_vent_state_mod1.Day.values),
                        max_date_allowed=max(df_vent_state_mod1.Day.values),
                        date=oneWeekFromNow,
                        initial_visible_month=oneWeekFromNow,
                        style={'margin-bottom':20}
                    ),
                    id="date-projections-picker-div"
                ),
                html.H6('Predicted Value:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'us_map_dropdown-vent',
                        options = [{'label': x, 'value': x} for x in state_cols],
                        value = 'Demand',
                    ),
                ),
            ],
            ),
            dbc.Col(
            [
                html.Div(
                    id = 'us_map_projections_vent',
                    children = [],
                ),
            ]
            )
        ]
        ),
        dbc.Row(
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
            ]
            )
        ]
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                    id = 'time_x_graph',
                    children = [],
                    style={
                        'width': '100%',
                        'display': 'inline-block',
                        }
                ),
            ]
            )
        ]
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6("""\
                        We propose......
                       """),
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
                        min_date_allowed=min(df_vent_transfers_mod1.Day.values),
                        max_date_allowed=max(df_vent_transfers_mod1.Day.values),
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
                        options = [{'label': x, 'value': x} for x in ["Demand","Supply"]],
                        value = 'Demand',
                    ),
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Param1:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'p1-transfer-dropdown',
                        options = [{'label': change2Percent(x), 'value': x} for x in df_vent_transfers_mod1.Param1.unique()],
                        value = '0.1',
                    ),
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Param2:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'p2-transfer-dropdown',
                        options = [{'label': x, 'value': x} for x in df_vent_transfers_mod1.Param2.unique()],
                        value = '0.1',
                    ),
                ),
            ]
            ),
            dbc.Col(
            [
                html.H6('Param3:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'p3-transfer-dropdown',
                        options = [{'label': x, 'value': x} for x in df_vent_transfers_mod1.Param3.unique()],
                        value = '0.9',
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
            )
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Transfer:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'transfer-to-from-dropdown',
                        options = [{'label': x, 'value': x} for x in ["to", "from"]],
                        value = 'to',
                    ),
                ),
                html.Div(
                    dcc.Dropdown(
                        id = 'transfer-state-dropdown',
                        options = [{'label': x, 'value': x} for x in models],
                        value = 'Washington IHME',
                    ),
                ),
                html.Div(
                    id = 'transfer_list',
                    children = [],
                ),
            ]
            ),
        ],
        ),
        dbc.Row([
                dbc.Col(
                    html.H6('Base Model:',id="date-projections"),
                    html.Div(
                        dcc.Dropdown(
                            id = 'base-model-dropdown_download',
                            options = [{'label': x, 'value': x} for x in models],
                            value = 'Washington IHME',
                        ),
                    ),
                ),
    			dbc.Col(
    				html.Div(
    					html.A(
    						"Download the Ventilator Demand Data",
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
    						"Download the Ventilator Tranfers Data",
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


def build_us_vent_map(chosen_model,chosen_date,val):
    global df_vent_state_mod1, df_vent_state_mod2
    if chosen_model == "Washington IHME":
        df_map = df_vent_state_mod1
    else:
        df_map = df_vent_state_mod2

    if isinstance(chosen_date, str):
        chosen_date = datetime.datetime.strptime(chosen_date, '%Y-%m-%d').date()

    df_map = df_map.loc[df_map['Date']==chosen_date]
    df_map = df_map.loc[df_map['State']!='US']
    df_map = df_map.applymap(str)

    df_map.loc[:,'code'] = df_map.State.apply(lambda x: states[x])

    fig = go.Figure()

    df_map.loc[:,'text'] = df_map['State'] + '<br>' + \
                'Supply Excess ' + df_map['Supply_Excess'] + '<br>' + \
                'Supply ' + df_map['Supply'] + '<br>' + \
                'Demand ' + df_map['Demand']

    fig = go.Figure(data=go.Choropleth(
            locations=df_map['code'],
            z=df_map[val].astype(float),
            locationmode='USA-states',
            colorscale='Inferno_r',
            autocolorscale=False,
            text=df_map['text'], # hover text
            marker_line_color='white', # line markers between states
            colorbar_title='{}'.format(val)
        ))

    fig.update_layout(
            title_text=add_cases('{} Predicted {}'.format(chosen_date.strftime('%b %d,%Y'), val)),
            geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'
            ),
        )

    graph = dcc.Graph(
        id='projection-map-vent',
        figure=fig
    )
    return graph


def build_us_vent_timeline(chosen_model):
    global df_vent_state_mod1, df_vent_state_mod2
    if chosen_model == "Washington IHME":
        df_projections_sub = df_vent_state_mod1
    else:
        df_projections_sub = df_vent_state_mod2

    df_projections_sub = df_projections.loc[df_projections.State == 'US']
    fig = go.Figure()

    for i,val in enumerate(state_cols):
        fig.add_trace(go.Scatter(
            x=df_projections_sub['Date'],
            y=df_projections_sub[val].values,
            legendgroup=i,
            name=val.replace(' ','<br>'),
            mode="lines+markers",
            marker=dict(color=colors[i]),
            line=dict(color=colors[i])
        ))
        i+=1

    fig.update_layout(
                height=550,
                title={
                    'text': '<b> US Ventilator Predictions </b>',
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Date",'linecolor': 'lightgrey'},
                yaxis={'title': "Count",'linecolor': 'lightgrey'},
                legend_title='<b> Values Predicted </b>',
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend={
                        "orientation": "h",
                        "xanchor": "center",
                        "y": -0.2,
                        "x": 0.5
                        }
            )

    graph = dcc.Graph(
        id='projection-graph-vent',
        figure=fig
    )
    return graph


def build_us_vent_peaks(chosen_model,val):
    global df_vent_state_mod1, df_vent_state_mod2
    if chosen_model == "Washington IHME":
        df_peaks = df_vent_state_mod1
    else:
        df_peaks = df_vent_state_mod2

    df_peaks = df_peaks.loc[:,["State","Date",val]]
    idx = df_peaks.groupby(['State'])[val].transform(max) == df_peaks[val]
    df_peaks = df_peaks[idx]
    df_peaks.at[:,'StateValue'] = df_peaks.apply(lambda x: x.State + ':' + str(x.Demand),axis=1)
    df_peaks = df_peaks.loc[:,["Date","StateValue"]]
    df_peaks = df_peaks.groupby('Date')['StateValue'].apply(list)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_peaks['Date'],
        y=[0]*len(df_peaks),
        mode="markers",
        text=df_peaks['StateValue'][1:-1].replace(',','<br>'),
    ))

    fig.update_layout(
                title={
                    'text': '<b> US Ventilator Peaks Per State </b>',
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Date",'linecolor': 'lightgrey'},
                yaxis={'title': "Count",'linecolor': 'lightgrey'},
                legend_title='<b> Values Predicted </b>',
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend={
                        "orientation": "h",
                        "xanchor": "center",
                        "y": -0.2,
                        "x": 0.5
                        }
            )

    graph = dcc.Graph(
        id='projection-graph-vent',
        figure=fig
    )
    return graph


def build_us_transfers_map(chosen_model,chosen_date,val,p1,p2,p3):
    global df_vent_transfers_mod1, df_vent_transfers_mod2
    if chosen_model == "Washington IHME":
        df_trans_map = df_vent_transfers_mod1
    else:
        df_trans_map = df_vent_transfers_mod2

    #filter on date
    df_trans_map = df_trans_map.loc[df_trans_map['Date']==chosen_date]
    df_trans_map = df_trans_map.applymap(str)

    #filter on three params
    df_trans_map = df_trans_map.loc[df_trans_map['Param1']==p1]
    df_trans_map = df_trans_map.loc[df_trans_map['Param2']==p2]
    df_trans_map = df_trans_map.loc[df_trans_map['Param3']==p3]

    fig = go.Figure()

    #add num units for state to and subtract from state from
    df_map_to = df_map.groupby('State_To', as_index=False)['Num_Units'].sum()
    df_map_from = df_map.groupby('State_From', as_index=False)['Num_Units'].sum()
    df_map_to.columns = ['State','Num_Units_to']
    df_map_from.columns = ['State','Num_Units_from']
    df_tranfers = pd.merge(df_map_to,df_map_from,on='State',how='outer')
    df_tranfers = df_tranfers.fillna(0)
    df_tranfers.loc[:,"Units"] = df_tranfers.apply(lambda x: x.Num_Units_to - x.Num_Units_from)
    df_tranfers = df_tranfers.loc[["State","Units"]]
    #if demand is chosen, show number as is. otherwise show -1*number
    if val == "Supply":
        df_tranfers["Units"] = -1 * df_tranfers["Units"]
    df_tranfers.loc[:,'code'] = df_tranfers.State.apply(lambda x: states[x])

    df_tranfers.loc[:,'text'] = df_tranfers['State'] + '<br>' + \
                'Units ' + df_tranfers['Units']

    fig = go.Figure(data=go.Choropleth(
            locations=df_tranfers['code'],
            z=df_tranfers['Units'].astype(float),
            locationmode='USA-states',
            colorscale='Inferno_r',
            autocolorscale=False,
            text=df_tranfers['text'], # hover text
            marker_line_color='white', # line markers between states
            colorbar_title='{}'.format(val)
        ))

    fig.update_layout(
            title_text=add_cases('{} Predicted {}'.format(chosen_date.strftime('%b %d,%Y'), val)),
            geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'
            ),
        )

    graph = dcc.Graph(
        id='projection-map-vent-transfers',
        figure=fig
    )
    return graph

def build_transfers(chosen_model,to_or_from):
    global df_vent_transfers_mod1, df_vent_transfers_mod2
    if chosen_model == "Washington IHME":
        df_trans = df_vent_transfers_mod1
    else:
        df_trans = df_vent_transfers_mod2
    if to_or_from == "to":
        return [{'label': x, 'value': x} for x in df_trans.State_To.unique()]
    else:
        return [{'label': x, 'value': x} for x in df_trans.State_From.unique()]

def build_us_transfers(chosen_model,chosen_date,to_or_from,state):
    global df_vent_transfers_mod1, df_vent_transfers_mod2
    if chosen_model == "Washington IHME":
        df_trans = df_vent_transfers_mod1
    else:
        df_trans = df_vent_transfers_mod2

    df_trans = df_trans.loc[df_trans['Day']==chosen_date]
    if to_or_from == "to":
        df_trans = df_trans.loc[df_trans['State_To']==state]
        df_trans = df_trans[["State_From","Num_Units"]]
        df_trans.columns = ["State","Units"]
    else:
        df_trans = df_trans.loc[df_trans['State_From']==state]
        df_trans = df_trans[["State_From","Num_Units"]]
        df_trans.columns = ["State","Units"]

    tab_transfers = dash_table.DataTable(
            id="transfer_list",
            data=df_trans.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_trans.columns,
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_table={
                'overflowX': 'auto',
                'maxHeight': '400px',
                'overflowY': 'auto',
                'border': 'thin lightgrey solid',
            },
            style_cell={
                'height': 'auto',
                'minWidth': '0px',
                'width': '180px',
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
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            fixed_rows={ 'headers': True, 'data': 0 },
        )
    return tab_transfers

def build_download_link_demand(chosen_model):
    global df_vent_state_mod1, df_vent_state_mod2
    if chosen_model == "Washington IHME":
        state_csv_string = df_vent_state_mod1.to_csv(index=False, encoding='utf-8')
    else:
        state_csv_string = df_vent_state_mod1.to_csv(index=False, encoding='utf-8')
    state_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(state_csv_string)
    return state_csv_string

def update_download_link_transfers(chosen_model):
    global df_vent_transfers_mod1, df_vent_transfers_mod2
    if chosen_model == "Washington IHME":
        transfers_csv_string = df_vent_transfers_mod1.to_csv(index=False, encoding='utf-8')
    else:
        transfers_csv_string = df_vent_transfers_mod1.to_csv(index=False, encoding='utf-8')
    transfers_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(transfers_csv_string)
    return transfers_csv_string

def VentilatorAllocations():
    layout = html.Div([nav, body, footer],className="site")
    return layout
