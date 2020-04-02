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

cols = ['Current Active','Current Hospitalized','Total Detected','Total Hospitalized','Total Detected Deaths']

def remove_words(w):
    return w.replace('Current ','')

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
              html.H1("COVID-19"),
              html.H2("Projections")
              ]
            ),
          ],
        ),
        dbc.Row(
          [
            dbc.Col(
              [
              html.H6('Date:'),
              html.Div(
                    dcc.DatePickerSingle(
                        id='us-map-date-picker-range',
                        min_date_allowed=min(df_projections.Day.values),
                        max_date_allowed=max(df_projections.Day.values),
                        date=oneWeekFromNow,
                        initial_visible_month=oneWeekFromNow,
                        style={'margin-bottom':10}
                    )
                ),
                html.H6('Predicted Value:'),
                    html.Div(dcc.Dropdown(
                        id = 'us_map_dropdown',
                        options = [{'label': x, 'value': x} for x in cols],
                        value = 'Current Active',
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
             dbc.Col(html.Div(dcc.Dropdown(
                 id = 'state_dropdown',
                 options = [{'label': x, 'value': remove_words(x)} for x in df_projections.State.unique()],
                 value = 'US',
                 style={'width': '50%', 'display' : 'inline-block','margin':0, 'textAlign': 'left'})
               ))
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

def build_us_map(map_date,val='Current Active'):

    global df_projections

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date()

    df_map = df_projections.loc[df_projections['Day']==map_date]
    df_map = df_map.applymap(str)

    df_map.loc[:,'code'] = df_map.State.apply(lambda x: states[x])

    fig = go.Figure()

    df_map.loc[:,'text'] = df_map['State'] + '<br>' + \
                'Total Detected ' + df_map['Total Detected'] + '<br>' + \
                'Current Active ' + df_map['Current Active'] + '<br>' + \
                'Current Hospitalized ' + df_map['Current Hospitalized'] + '<br>' + \
                'Total Hospitalized ' + df_map['Total Hospitalized'] + '<br>' + \
                'Total Detected Deaths ' + df_map['Total Detected Deaths']

    fig = go.Figure(data=go.Choropleth(
            locations=df_map['code'],
            z=df_map[val].astype(float),
            locationmode='USA-states',
            colorscale='Inferno_r',
            autocolorscale=False,
            text=df_map['text'], # hover text
            marker_line_color='white', # line markers between states
            colorbar_title='{}'.format(remove_words(val))
        ))

    fig.update_layout(
            title_text=add_cases('{} Predicted {}'.format(map_date.strftime('%b %d,%Y'), remove_words(val))),
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
                width=1100,
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
