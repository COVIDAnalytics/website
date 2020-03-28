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
## Navbar
from navbar import Navbar
df = pd.read_csv('data/0327.csv')
df = df.loc[:,["Country","Median Age","Mortality"]]
#df.at[:,"Mortality"] = df.Mortality.apply(lambda x: x[:-1])
#df['Mortality'] = df['Mortality'].astype(float)
df = df.dropna()

nav = Navbar()

header = html.H3(
    'Select the Country'
)

options = [{'label': x, 'value': x} for x in set(df.Country.values)]

dropdown = html.Div(dcc.Dropdown(
    id = 'pop_dropdown',
    options = options,
    value = 'China'
))

output = html.Div(id = 'output',
                children = [],
                )

def App():
    layout = html.Div([
        nav,
        header,
        dropdown,
        output
    ])
    return layout

def build_graph(country):
    data = [go.Scatter(x = df.loc[df.Country == country]["Median Age"],
                            y = df.loc[df.Country == country]["Mortality"],
                            marker = {'color': 'orange'})]
    graph = dcc.Graph(
               figure = {
                   'data': data,
    'layout': go.Layout(
                        title = '{} Median Age vs Mortality'.format(country),
                        yaxis = {'title': 'Mortality Percentage'},
                        hovermode = 'closest'
                                      )
                           }
                 )
    return graph
