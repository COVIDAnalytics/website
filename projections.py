### Data
import pandas as pd
import pickle
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

nav = Navbar()

# all into one csv should be done offline
df_projections_1 = pd.read_csv('data/predicted/Prediction_NewYork.csv', sep=",", parse_dates = ['Day'])
df_projections_2 = pd.read_csv('data/predicted/Prediction_Massachusetts.csv', sep=",", parse_dates = ['Day'])
df_projections_3 = pd.read_csv('data/predicted/Prediction_Connecticut.csv', sep=",", parse_dates = ['Day'])
df_projections_1['State'] = 'New York'
df_projections_2['State'] = 'Massachusetts'
df_projections_3['State'] = 'Connecticut'
df_projections = pd.concat([df_projections_1,df_projections_2,df_projections_3])
today = pd.Timestamp('today')
df_projections = df_projections[df_projections['Day']>=today]

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
             dbc.Col(html.H4('State:'), width=1),
             dbc.Col(html.Div(dcc.Dropdown(
                 id = 'state_dropdown',
                 options = [{'label': x, 'value': x} for x in df_projections.State.unique()],
                 value = 'New York',
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
        if val != 'Day' and val != 'State' and val != 'Total Detected':
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
