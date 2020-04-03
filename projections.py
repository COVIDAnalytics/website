### Data
import pandas as pd
import pickle
import datetime
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar
from assets.colMapping import states

nav = Navbar()

df_projections = pd.read_csv('data/predicted/Allstates.csv', sep=",", parse_dates = ['Day'])
today = pd.Timestamp('today')
oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)
df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
df_projections = df_projections.loc[df_projections['Day']>=today]

cols = ['Active','Active Hospitalized','Total Detected','Cumulative Hospitalized','Total Detected Deaths']

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
                html.H1("COVID-19 Analytics"),
                html.H2("Projections"),
                html.P("""\
                        This page presents the predictions of a new epidemiological model for COVID-19 infections, hospitalizations, and deaths in all states of the United States. The model is based on the widely successful SEIR (Susceptible-Exposed-Infected-Recovered) model, which allocates every person to one of four states:
                       """),
                dcc.Markdown('''
                  1. Susceptible: The general population that has not been infected and is not immune.
                  2. Exposed: People who are currently infected, but are not contagious and lie within the incubation period.
                  3. Infected: People who are currently infected and are contagious.
                  4. Recovered: People who recovered and are immune.
                '''),
                html.P("""\
                        The SEIR model is then, using various parameters, able to produce the dynamics of a pandemic as people move between these states. This base model is then greatly expanded and adjusted for many factors important in the current COVID-19 pandemic, including under-detection, hospitalization, and societal counteracting measures. The  parameter values are taken from the meta-analysis from the papers that the group curated. Important parameters are varied across different states:
                      """),
                dcc.Markdown('''
                  1. Effective contact rate: The effective contact rate measures the number of people that comes into contact with an infected person per day. This fundamental quantity largely controls the spread of the virus, and would be higher in densely populated states (such as NY, CT) and smaller in sparsely populated ones (e.g. AZ, NV).
                  2. Societal/Governmental Response: This parameter measures, through a parametric nonlinear function, the impact of the governmental and societal response on the spread of the virus over time. This covers measures including government decrees on social distancing and shelter-in-place, but also increased hygiene awareness and reduced travel among the general population. This function is fitted for every state to account for the differing responses in different states.
                '''),
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
                        style={'margin-bottom':20}
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
                    'text-align': 'center',
                    'font-size': 30,
                    'font-weight':'bold'
                    }
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(dbc.Card([], id = 'us_tot_det', color="dark", inverse=True, style={'margin-top':20,'margin-bottom':20}),width="auto"),
            dbc.Col(dbc.Card([], id = 'us_tot_death', color="dark", inverse=True, style={'margin-top':20,'margin-bottom':20}),width="auto"),
            dbc.Col(dbc.Card([], id = 'us_active', color="dark", inverse=True, style={'margin-top':20,'margin-bottom':20}),width="auto"),
            dbc.Col(dbc.Card([], id = 'us_active_hosp', color="dark", inverse=True, style={'margin-top':20,'margin-bottom':20}),width="auto"),
        ]
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.H6('Predicted Value:'),
                    html.Div(dcc.Dropdown(
                        id = 'us_map_dropdown',
                        options = [{'label': x, 'value': x} for x in cols],
                        value = 'Active',
                        style={'width': '100%','margin-bottom':10}
                    ),
                ),
                html.P('* Gray states correspond to no projection as their number \
                        of confirmed cases so far is too low for a reliable estimation.\
        		        We will update on a daily basis.',
                        style={'color':'gray'}
                ),
            ],
            width=3
            ),
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
             dbc.Col(html.H4('State:'), width=1),
             dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id = 'state_dropdown',
                        options = [{'label': x, 'value': x} for x in df_projections.State.unique()],
                        value = 'US',
                        style={'width': '50%', 'display' : 'inline-block','margin':0, 'textAlign': 'left'}
                    )
               )
             )
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
   ],
   className="projections-body",
)

def ProjectState():
    layout = html.Div(
    [
        nav,
        body
    ])
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
                lakecolor='rgb(255, 255, 255)'),
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

    colors = [
    '#1f77b4',  # muted blue
    '#9467bd',  # muted purple
    '#e377c2',  # raspberry yogurt pink
    '#2ca02c',  # cooked asparagus green
    '#ff7f0e',  # safety orange
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
    ]

    for i,val in enumerate(df_projections_sub.columns):
        if val in cols and val != 'Total Detected':
            fig.add_trace(go.Scatter(
                x=df_projections_sub['Day'],
                y=df_projections_sub[val].values,
                legendgroup=i,
                name=val,
                mode="lines+markers",
                marker=dict(color=colors[i]),
                line=dict(color=colors[i])
            ))

    fig.update_layout(
                height=550,
                title={
                    'text': '<b> {} </b>'.format(state),
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Date"},
                yaxis={'title': "Count"},
                legend_title='<b> Values Predicted </b>',
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest')

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
            style={"text-align":"center","font-size":30,"font-weight": "bold","color":"#1E74F0"}
        ),
        dbc.CardBody(
            [
                html.H5(val,id='us-stats-cards'),
            ]
        ),
    ]
    return card_content
