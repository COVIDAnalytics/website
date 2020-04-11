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
                html.P("""\
                        This page presents the predictions of a new epidemiological model, \
                        DELPHI, for COVID-19 infections, hospitalizations, and deaths in all \
                        states of the United States. The model is based on the widely applied \
                        SEIR (Susceptible-Exposed-Infected-Recovered) modeling approach. \
                        We additionally explicitly account for under detection and government \
                        intervention on a state level.
                       """),
                dcc.Markdown(''' **Note on "Active Cases"**: Active Cases is the estimated number of COVID-19 \
                cases that have not recovered or perished yet. The seemingly large discrepancy \
                with what the JHU dashboard indicates is because JHU does not have data on the \
                number of people recovered for most states, and thus the number of people \
                recovered recorded there is a vast underestimate.'''),
                dcc.Markdown('''You can read a summary of the documentation \
                [here](/projections_documentation) or access\
                 or [source code](https://github.com/COVIDAnalytics/epidemic-model).'''),
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [

                    dcc.Markdown("""**Note on Active**: Active is the estimated number of COVID-19 cases that have not recovered or perished yet.
                          The seemingly large discrepancy with what the JHU dashboard indicates is because JHU does
                          not have data on the number of people recovered for most states, and thus the number of
                          people recovered recorded there is a vast underestimate. """),
            ]
            )
        ]
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
            dbc.Col(
            [
                html.H6('Predicted Value:',id="date-projections"),
                    html.Div(
                        dcc.Dropdown(
                            id = 'us_map_dropdown',
                            options = [{'label': x, 'value': x} for x in cols],
                            value = 'Total Detected',
                        ),
                    ),
            ],
            ),
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

def build_us_map(map_date,val='Total Detected'):

    global df_projections

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date()

    if val is not None:

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
                colorbar_title='{}'.format(add_cases(val))
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


def build_state_projection(state,val='Total Detected'):
    global df_projections

    df_projections_sub = df_projections.loc[df_projections.State == state]
    fig = go.Figure()
    color_dict={'Total Detected':0,'Active':1,'Active Hospitalized':2,
                'Cumulative Hospitalized':3,'Total Detected Deaths':4};
    if val is not None:
        i = color_dict[val]
        fig.add_trace(go.Scatter(
            x=df_projections_sub['Day'],
            y=df_projections_sub[val].values,
            legendgroup=i,
            name=val.replace(' ','<br>'),
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
                html.H5(add_cases(val),id='us-stats-cards'),
            ]
        ),
    ]
    return card_content
