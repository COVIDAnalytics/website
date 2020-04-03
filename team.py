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
import yaml

nav = Navbar()


# Load team members
with open("assets/team_members/team.yml") as f:
    members = yaml.load(f, Loader=yaml.FullLoader)
num_members = len(members)
members_per_row = 4


# Single member pic
def member_pic(member):
    return dbc.Col([html.Div([html.Img(src='assets/team_members/photos/%s' % member['photo']),
                              dbc.Button(member['name'], color="info", block=True,
                                         className="mb-3", href=member['website'])],
                                         style={'display': 'inline-block'})],
                   width=3)

# Table rows
member_rows = [dbc.Row([member_pic(m) for m in members[i*members_per_row:(i+1)*members_per_row]])
               for i in range(num_members//members_per_row)] + \
              [dbc.Row([member_pic(m) for m in members[num_members - (num_members % members_per_row):]])]


body = dbc.Container([dbc.Row([dbc.Col([html.H1("COVID-19 Analytics"),
                                        html.H5("Our team comprises passionate researchers in Operations Research and Analytics!")])])] +
                     member_rows)

def Team():
    layout = html.Div(
    [
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Team()
app.title = "MIT_ORC_COVID19"
