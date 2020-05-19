import yaml
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

def Contact():

    # Form details
    formspree_url="https://formspree.io/xqkdkggg"
    mailing_list="covidanalytics@mit.edu"


    nav = Navbar()
    footer = Footer()

    name_input = dbc.FormGroup(
        [
            dbc.Row(
            [
                dbc.Col(html.Label("Topic", htmlFor="name-row"),width="auto"),
                dbc.Col(
                    dcc.Input(
                        type="text",
                        id="name-row",
                        name="name",
                        className="form-control",
                        placeholder="Enter the topic of your message",
                        style={"width":"50%"},
                    ),
                    width=True
                ),
            ],
            )
        ],
    )

    email_input = dbc.FormGroup(
        [
            dbc.Row(
            [
                dbc.Col(html.Label("Email", htmlFor="email-row"),width="auto"),
                dbc.Col(
                    [dcc.Input(
                        type="email",
                        id="email-row",
                        name="email",
                        className="form-control",
                        placeholder="Enter your email address",
                        style={"width":"50%"}
                    ),
                    dcc.Input(
                        type="hidden",
                        name="_subject",
                        value="Covidanalytics Mailing List",
                        style={"width":"50%"},
                    )
                ],
                width=True
                ),
            ],
            )
        ],
    )


    text_input = dbc.FormGroup(
        [
            dbc.Row(
            [
                dbc.Col(dbc.Label("Text", html_for="message-row"),width="auto"),
                dbc.Col(
                [
                    dcc.Textarea(
                        placeholder="Your message goes here...",
                        className="form-control",
                        id="message-row",
                        name="message",
                        style={"width":"50%","marginLeft":5},
                    )
                ],
                width=True
                ),
            ],
            )
        ],
    )

    submit_button = html.Button("Submit", className="btn btn-primary", formEncType="submit")

    form = html.Form([name_input, email_input, text_input, submit_button],
                     action=formspree_url,
                     method="POST")

    body = dbc.Container([
                dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P("We are happy to collaborate and help you take our research one step further. " +
                                   "Feel free to send us an email using the following form."),
                            html.P(
                                ["You can also reach out to us by sending an email to ",
                                    html.A(
                                            mailing_list,
                                            href="mailto:%s" % mailing_list,
                                        ), "."
                                ]
                            ),
                            form
                          ]
                        )
                    ],

                    )
                ],
                className="page-body",
    )

    layout = html.Div([nav, body, footer],className="site")
    return layout
