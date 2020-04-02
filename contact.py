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

email_input = dbc.FormGroup(
    [
        dbc.Label("Email", html_for="email-row", width=2),
        dbc.Col(
            dbc.Input(
                type="email", id="email-row", placeholder="Enter your email address"
            ),
            width=10,
        ),
    ],
    row=True,
)

topic_input = dbc.FormGroup(
    [
        dbc.Label("Name", html_for="topic-row", width=2),
        dbc.Col(
            dbc.Input(
                type="email",
                id="topic-row",
                placeholder="Enter the topic of your message",
            ),
            width=10,
        ),
    ],
    row=True,
)

text_input = dbc.FormGroup(
    [
        dbc.Label("Text", html_for="message-row", width=2),
        dbc.Col([
            dbc.Textarea(placeholder="Your message goes here...", 
                         ),
            dbc.FormText("Type something in the box above")],
            width=10,
          ),
        
    ],
    row=True,
)

submit_button = dbc.Button("Submit", color="primary")

form = dbc.Form([email_input, topic_input, text_input, submit_button])

body = dbc.Container([dbc.Row([dbc.Col([html.H1("COVID-19"),
                                        html.H5("We are happy to collaborate and help you take our research one step further."),
                                        html.H5("Feel free to send us an email using that the following form."),
                                        html.H5("You can also reach out to us by sending an email to covidanalytics@mit.edu."),
                                        form
                                         ])])])

def Contact():
    layout = html.Div(
    [
        nav,
        body,
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Contact()
app.title = "MIT_ORC_COVID19"
