### Data
import datetime
import pandas as pd

### Graphing
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from projections import df_projections
from assets.colMapping import states

nav = Navbar()

def build_us_map():

    global df_projections
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    df_map = df_projections.loc[df_projections['Day']==tomorrow]
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
            z=df_map['Current Active'].astype(float),
            locationmode='USA-states',
            colorscale='Reds',
            autocolorscale=False,
            text=df_map['text'], # hover text
            marker_line_color='white', # line markers between states
            colorbar_title='Tomorrow\'s Predictioned Active Counts'
        ))

    fig.update_layout(
            title_text='Tomorrow\'s Predictions of COVID-19 Cases',
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

body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H1("COVID-19"),
                     html.H2("Predictive Tools"),
                     html.P(
                         """\
                         MIT’s Operations Research Center provides open source interactive tools and dataset to predict patients outcome probabilities, including their potential Intensive Care Unit needs and expected length of stay in hospital.

                         We aim to rapidly develop, vet, and deliver tools for use by hospitals in the United States to combat the spread of COVID-19.

                         """
                           )
                   ],
                  width=3
               ),
                    dbc.Col(
                      [
                          html.Div(
                          id = 'us_map',
                          children = build_us_map(),
                          ),
                      ]
                      )
                 ],
            )
       ],
className="mt-4",
)

def Homepage():
    layout = html.Div([
                    nav,
                    body
                    ])
    return layout
