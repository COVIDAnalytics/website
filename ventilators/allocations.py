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

body = dbc.Container(
    [
    ],
   className="page-body"
)

def VentilatorAllocations():
    layout = html.Div([nav, body, footer],className="site")
    return layout
