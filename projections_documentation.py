### Data
import pandas as pd
import pickle
from datetime import datetime as dt
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import flask
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from navbar import Navbar
from footer import Footer
from interactive import demographics

nav = Navbar()
footer = Footer()

body = dbc.Container([
	dbc.Row(
        [
			dbc.Col([
				html.H1("COVID-19 Analytics"),
            	html.H2("Epidemiological Model Documentation"),
                html.P("""\
                        This page presents provides insights on a new epidemiological model for COVID-19 infections, hospitalizations, and deaths in all states of the United States. The model is based on the widely successful SEIR (Susceptible-Exposed-Infected-Recovered) model, which allocates every person to one of four states:
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
				 ])
		 ]
	 ),
])

def Projections_documentation():
    layout = html.Div([nav, body, footer])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Projections_documentation()
app.title = "COVIDAnalytics"
