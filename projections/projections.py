### Data
import pandas as pd
import datetime
import urllib

### Graphing
import plotly.graph_objects as go
import plotly.express as px
from textwrap import wrap
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

df_projections = pd.read_csv('data/predicted/Global_20200414.csv', sep=",", parse_dates = ['Day'])
today = pd.Timestamp('today')
oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)

df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
df_projections = df_projections.loc[df_projections['Day']>=today]
df_us = df_projections.loc[(df_projections.Country == "US") & (df_projections.Province != 'None')]

cols = ['Active','Active Hospitalized','Total Detected','Cumulative Hospitalized','Total Detected Deaths']

color_dict={'Total Detected':0,'Active':1,'Active Hospitalized':2,
                'Cumulative Hospitalized':3,'Total Detected Deaths':4};

map_locations = {'US', "Europe", "Asia", "North America", "South America", "Africa", 'World'}

dataset = "data/predicted/Global_20200412.csv"
data_csv_string = df_projections.to_csv(index=False, encoding='utf-8')
data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)

def add_cases(w):
    if 'Deaths' not in w:
        w += ' Cases'
    return w

def build_card(id):
    return dbc.Col(
                [
                dbc.Card(
                    [],
                    id = id,
                    color="dark",
                    inverse=True,
                    style={'marginBottom':20,'paddingTop':20,"height":"12rem"},
                    ),
                ],
                xs=12,
                sm=6,
                md=6,
                lg=3,
            )

body = dbc.Container(
    [
       dbc.Row(
        [
            dbc.Col(
            [
                html.H2("Projections"),
                dcc.Markdown("""\
                        A critical tool for COVID-19 planning is charting out the progression \
                        of the pandemic across the United States and the world. \
                        We've developed a new epidemiological model called DELPHI, which \
                        forecasts infections, hospitalizations, and deaths. \
                        You can think of our model as a standard \
                        [SEIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model) \
                        with additional \
                        features specific to the COVID-19 pandemic, like under-detection and \
                        differentiated government intervention.
                       """),
                dcc.Markdown('''If you want to learn more, check out the \
                             [documentation](/projections_documentation) or \
                             [source code](https://github.com/COVIDAnalytics/epidemic-model).'''),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                            html.H5("Note: what do we mean by \"active cases\"?"),
                            dcc.Markdown("We define a COVID-19 case as **active** \
                                         if it has not yet resulted in recovery \
                                         or death. You may notice a discrepancy \
                                         between the number of active cases here \
                                         and on the \
                                         [JHU map](https://coronavirus.jhu.edu/map.html). \
                                         The JHU map is very good at keeping track of new cases, \
                                         but does not always publish data on recovered cases, \
                                         which can lead to overestimating currently active \
                                         cases."),
                            html.H5("Disclaimer on death counts:"),
                            dcc.Markdown("The death counts for the non-US data is currently \
                            being refined and might be not accurate for some countries."),
                            ]
                        ),
                    ]
                ),
            ]
            ),
        ],
        ),

        html.Hr(),
        dbc.Row(
        [

            dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dcc.Markdown("For what date do you want to see projections?"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                dcc.DatePickerSingle(
                                                    id='us-map-date-picker-range',
                                                    min_date_allowed=min(df_us.Day.values),
                                                    max_date_allowed=max(df_us.Day.values),
                                                    date=oneWeekFromNow,
                                                    initial_visible_month=oneWeekFromNow,
                                                    style={'marginBottom':5,}
                                                ),
                                                id="date-projections-picker-div"
                                            ),
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
                                dcc.Markdown("And for which area?"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                [
                                                dcc.Dropdown(
                                                        id = 'location_map_dropdown',
                                                        options = [{'label': x, 'value': x} for x in map_locations],
                                                        value = 'US',
                                                ),

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
        dbc.Row(
        [
            build_card('us_tot_det'),
            build_card('us_tot_death'),
            build_card('us_active'),
            build_card('us_active_hosp')
        ],
        align="center"
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

                    id="predicted-value-projections-picker-div",
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
                    id = 'map_projections',
                    children = [],
                ),
                html.P('* Grey countries correspond to those that currently have insufficient data for projections or those in which the outbreak has ended.',
                        style={'color':'gray'}
                ),
            ]
            ),

        ],
        ),
        dbc.Row(
            [
                dbc.Col(
                [
                    html.H5('Use the tool below to explore our predictions for different locations.'),
                ]
                ),
            ],
        ),
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
                                                    options = [{'label': x, 'value': x} for x in cols],

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
                             'paddingTop': 20,
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

def build_continent_map(map_date,val='Active', continent = 'World'):
    global df_projections

    df_continent = df_projections
    if continent !='World':
        df_continent = df_projections.loc[df_projections.Continent == continent] #Filter by continent

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date() 

    df_map = df_continent.loc[df_continent['Day'] == map_date] 
    df_map = df_map.loc[df_map['Province'] == 'None'] #exclude province data
    df_map = df_map.loc[df_map['Country'] != 'None'] #exclude global world data
    df_map = df_map.applymap(str)

    fig = go.Figure()

    if (val is not None) and (val in cols):

        df_map.loc[:,'text'] = df_map['Country'] + '<br>' + \
                    'Total Detected ' + df_map['Total Detected'] + '<br>' + \
                    'Active ' + df_map['Active'] + '<br>' + \
                    'Active Hospitalized ' + df_map['Active Hospitalized'] + '<br>' + \
                    'Cumulative Hospitalized ' + df_map['Cumulative Hospitalized'] + '<br>' + \
                    'Total Detected Deaths ' + df_map['Total Detected Deaths']


        fig = go.Figure(data=go.Choropleth(
                locations=df_map['Country'],
                z=df_map[val].astype(float),
                locationmode="country names",
                autocolorscale=False,
                colorscale='inferno_r',
                text=df_map['text'], # hover text
                marker_line_color='black', # line markers between states
                colorbar_title='{}'.format(add_cases(val))
            ))

    fig.update_layout(
            margin=dict(l=10, r=10, t=50, b=50),
            title_text=add_cases('{} Predicted {} {}'.format(map_date.strftime('%b %d,%Y'), continent, val)),
            geo = dict(
                scope= continent.lower(),
                projection=go.layout.geo.Projection(type = 'natural earth'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)',
                countrycolor='lightgray',
                landcolor='whitesmoke',
                showland=True,
                showframe = False,
                showcoastlines = True,
                showcountries=True,
                visible = False,
            ),
        )

    graph = dcc.Graph(
        id='continent-projection-map',
        figure=fig,
    )

    return graph

def build_us_map(map_date,val='Active'):

    global df_us

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date()

    df_map = df_us.loc[df_us['Day']==map_date]
    df_map = df_map.loc[df_us['Province']!='US']
    df_map = df_map.applymap(str)

    df_map.loc[:,'code'] = df_map.Province.apply(lambda x: states[x])

    fig = go.Figure()

    if (val is not None) and (val in cols):

        df_map.loc[:,'text'] = df_map['Province'] + '<br>' + \
                    'Total Detected ' + df_map['Total Detected'] + '<br>' + \
                    'Active ' + df_map['Active'] + '<br>' + \
                    'Active Hospitalized ' + df_map['Active Hospitalized'] + '<br>' + \
                    'Cumulative Hospitalized ' + df_map['Cumulative Hospitalized'] + '<br>' + \
                    'Total Detected Deaths ' + df_map['Total Detected Deaths']

        fig = go.Figure(data=go.Choropleth(
                locations=df_map['code'],
                z=df_map[val].astype(float),
                locationmode='USA-states',
                colorscale='inferno_r',
                autocolorscale=False,
                text=df_map['text'], # hover text
                marker_line_color='white' , # line markers between states
                colorbar_title='{}'.format(add_cases(val))
            ))

    fig.update_layout(
            margin=dict(l=10, r=10, t=50, b=50),
            title_text=add_cases('{} Predicted US {}'.format(map_date.strftime('%b %d,%Y'), val)),
            geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'
            ),
        )

    graph = dcc.Graph(
        id='us-projection-map',
        figure=fig
    )   
    return graph

def find_smallest_scope(state, country, continent):
    location = state
    if state in 'None':
        if country is 'None':
            location = continent
        else:
            location = country
    return location

def build_state_projection(state, country, continent, vals):
    global df_projections
    location = find_smallest_scope(state, country, continent)

    df_projections_sub = df_projections.loc[ (df_projections.Province == state) & (df_projections.Country == country)]
    if continent not in ['US', 'World']:
        df_projections_sub = df_projections_sub.loc[(df_projections_sub.Continent == continent)]
    if continent == 'US':
        df_projections_sub = df_projections.loc[(df_projections.Country == 'US') & (df_projections.Province == state)]
    if continent == 'World':
        if country =='None':
            df_projections_sub = df_projections.loc[(df_projections.Continent == 'None')] #include only global world data
    fig = go.Figure()

    if (vals is not None) and (set(vals).issubset(set(cols))):
        for val in vals:
            i = color_dict[val]
            fig.add_trace(go.Scatter(
                name=val,
                showlegend=True,
                x=df_projections_sub['Day'],
                y=df_projections_sub[val].values,
                mode="lines+markers",
                marker=dict(color=colors[i]),
                line=dict(color=colors[i])
            ))

    title = '<br>'.join(wrap('<b> Projections for {} </b>'.format(location), width=26))
    fig.update_layout(
                height=550,
                title={
                    'text': title,
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Date",'linecolor': 'lightgrey'},
                yaxis={'title': "Count",'linecolor': 'lightgrey'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )

    graph = dcc.Graph(
        id='projection-graph',
        figure=fig
    )
    return graph

def get_stat(d, val, scope):
    global df_projections
    df_projections_sub = df_projections

    if isinstance(d, str):
        d = datetime.datetime.strptime(d, '%Y-%m-%d').date()

    if scope == 'US':
        df_projections_sub = df_projections.loc[(df_projections.Country == scope) & (df_projections.Province == 'None')]
    elif scope =='World':
        df_projections_sub = df_projections.loc[df_projections.Continent == 'None']
    else:
        df_projections_sub = df_projections.loc[(df_projections.Continent == scope) & (df_projections.Country == 'None')]

    df_projections_sub = df_projections_sub.loc[df_projections_sub['Day']==d].reset_index()

    card_content = [
        dbc.CardHeader(
            f'{df_projections_sub.iloc[0][val]:,}',
            style={"textAlign":"center","fontSize":30,"fontWeight": "bold","color":'#1E74F0'}
        ),
        dbc.CardBody(
            [
                html.H5(add_cases(val),id='us-stats-cards'),
            ]
        ),
    ]
    return card_content
