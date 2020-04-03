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


# Form details
formspree_url="https://formspree.io/xqkdkggg"
mailing_list="covidanalytics@mit.edu"



nav = Navbar()
name_input = dbc.FormGroup(
    [
        dbc.Col(html.Label("Topic", htmlFor="name-row"), width=1),
        dbc.Col(
            dcc.Input(
                type="text",
                id="name-row",
                name="name",
                className="form-control",
                placeholder="Enter the topic of your message",
            ),
            width=6,
        ),
    ],
    row=True,
)

email_input = dbc.FormGroup(
    [
        dbc.Col(html.Label("Email", htmlFor="email-row"), width=1),
        dbc.Col(
            [dcc.Input(
                type="email",
                id="email-row",
                name="email",
                className="form-control",
                placeholder="Enter your email address"),
            dcc.Input(
                type="hidden",
                name="_subject",
                value="Covidanalytics Mailing List")]
            ,
            width=6,
        ),
    ],
    row=True,
)


text_input = dbc.FormGroup(
    [
        dbc.Label("Text", html_for="message-row", width=1),
        dbc.Col([ dcc.Textarea(placeholder="Your message goes here...",
            className="form-control",
            id="message-row",
            name="message")],
            width=6),
    ],
    row=True,
)

submit_button = html.Button("Submit", className="btn btn-primary", formEncType="submit")

form = html.Form([name_input, email_input, text_input, submit_button],
                 action=formspree_url,
                 method="POST")

body = dbc.Container([dbc.Row([dbc.Col([html.H1("COVID-19 Analytics"),
                                        html.P("We are happy to collaborate and help you take your research one step further. " +
                                               "Feel free to send us an email using the following form."),
                                        html.P(["You can also reach out to us by sending an email to ", html.A(
                                            mailing_list, href="mailto:%s" % mailing_list, ), "."]),
                                        form
                                        ])])])

def Contact():
    layout = html.Div( [nav, body])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Contact()
app.title = "MIT_ORC_COVID19"
