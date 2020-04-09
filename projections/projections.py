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

df_projections = pd.read_csv('data/predicted/Allstates.csv', sep=",", parse_dates = ['Day'])
today = pd.Timestamp('today')
oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)
df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
df_projections = df_projections.loc[df_projections['Day']>=today]

cols = ['Active','Active Hospitalized','Total Detected','Cumulative Hospitalized','Total Detected Deaths']


dataset = "data/predicted/Allstates.csv"
data_csv_string = df_projections.to_csv(index=False, encoding='utf-8')
data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)

def add_cases(w):
    if 'Deaths' not in w:
        w += ' Cases'
    return w

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                html.H2("Projections"),
                html.P("""\
                        This page presents the predictions of a new epidemiological model for COVID-19 infections, \
                        hospitalizations, and deaths in all states of the United States. The model is based on the widely \
                        applied SEIR (Susceptible-Exposed-Infected-Recovered) modeling approach.
                       """),
                dcc.Markdown('''You can read more about the model [here](/projections_documentation).'''),
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Date:',id="date-projections"),
                html.Div(
                    dcc.DatePickerSingle(
                        id='us-map-date-picker-range',
                        min_date_allowed=min(df_projections.Day.values),
                        max_date_allowed=max(df_projections.Day.values),
                        date=oneWeekFromNow,
                        initial_visible_month=oneWeekFromNow,
                        style={'marginBottom':20}
                    ),
                    id="date-projections-picker-div"
                ),
            ],
            ),
        ]
        ),
        dbc.Row(
        [
            html.Div(
                id='us-stats-title',
                style={
                    'width': '100%',
                    'color': 'black',
                    'textAlign': 'center',
                    'fontSize': 30,
                    'fontWeight':'bold'
                    }
            ),
        ],
        ),
        dbc.CardDeck(
        [
            dbc.Card([], id = 'us_tot_det', color="dark", inverse=True, style={'marginBottom':20,'paddingTop':20}),
            dbc.Card([], id = 'us_tot_death', color="dark", inverse=True, style={'marginBottom':20,'paddingTop':20}),
            dbc.Card([], id = 'us_active', color="dark", inverse=True, style={'marginBottom':20,'paddingTop':20}),
            dbc.Card([], id = 'us_active_hosp', color="dark", inverse=True, style={'marginBottom':20,'paddingTop':20}),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Predicted Value:',id="date-projections"),
                    html.Div(
                        dcc.Dropdown(
                            id = 'us_map_dropdown',
                            options = [{'label': x, 'value': x} for x in cols],
                            value = 'Active',
                        ),
                    ),
            ],
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                    id = 'us_map_projections',
                    children = [],
                ),
            ]
            )
        ],
        ),
        dbc.Row(
        [
            html.P('* Gray states correspond to no projection as their number \
                    of confirmed cases so far is too low for a reliable estimation.\
                    We will update on a daily basis.',
                    style={'color':'gray'}
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('State:',id="date-projections"),
                html.Div(
                    dcc.Dropdown(
                        id = 'state_dropdown',
                        options = [{'label': x, 'value': x} for x in df_projections.State.unique()],
                        value = 'US',
                    )
               )
            ],
            ),
        ],
        ),
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
                             }
                     ),
                ]
                )
          ],
          ),
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
   ],
   className="page-body"
)

def ProjectState():
    layout = html.Div([nav, body, footer],className="site")
    return layout

def build_us_map(map_date,val='Active'):

    global df_projections

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date()

    df_map = df_projections.loc[df_projections['Day']==map_date]
    df_map = df_map.loc[df_projections['State']!='US']
    df_map = df_map.applymap(str)

    df_map.loc[:,'code'] = df_map.State.apply(lambda x: states[x])

    fig = go.Figure()

    df_map.loc[:,'text'] = df_map['State'] + '<br>' + \
                'Total Detected ' + df_map['Total Detected'] + '<br>' + \
                'Active ' + df_map['Active'] + '<br>' + \
                'Active Hospitalized ' + df_map['Active Hospitalized'] + '<br>' + \
                'Cumulative Hospitalized ' + df_map['Cumulative Hospitalized'] + '<br>' + \
                'Total Detected Deaths ' + df_map['Total Detected Deaths']

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
            title_text=add_cases('{} Predicted {}'.format(map_date.strftime('%b %d,%Y'), val)),
            geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'
            ),
        )

    graph = dcc.Graph(
        id='projection-map',
        figure=fig
    )
    return graph


def build_state_projection(state):
    global df_projections

    df_projections_sub = df_projections.loc[df_projections.State == state]
    fig = go.Figure()

    i = 0
    for val in df_projections_sub.columns:
        if val in cols and val != 'Total Detected':
            fig.add_trace(go.Scatter(
                x=df_projections_sub['Day'],
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
                    'text': '<b> {} </b>'.format(state),
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
        id='projection-graph',
        figure=fig
    )
    return graph

def get_us_stat(d, val):
    global df_projections

    if isinstance(d, str):
        d = datetime.datetime.strptime(d, '%Y-%m-%d').date()

    us_date = df_projections.loc[(df_projections['Day']==d) & (df_projections['State']=='US')].reset_index()

    card_content = [
        dbc.CardHeader(
            f'{us_date.iloc[0][val]:,}',
            style={"textAlign":"center","fontSize":30,"fontWeight": "bold","color":"#1E74F0"}
        ),
        dbc.CardBody(
            [
                html.H5(val,id='us-stats-cards'),
            ]
        ),
    ]
    return card_content
