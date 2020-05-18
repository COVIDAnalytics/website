import yaml

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

def Press():
    with open("assets/press/important_press.yml") as f:
        key_article = yaml.load(f, Loader=yaml.FullLoader)
    num_key_articles = len(key_article)

    with open("assets/press/press.yml") as f:
        article = yaml.load(f, Loader=yaml.FullLoader)
    num_articles = len(article)

    nav = Navbar()
    footer = Footer()

    def build_card(a):
        card_content = \
                [
                    dbc.CardHeader(
                            [
                                html.H6(a['date'],className="press-date") if a['date'] != "ongoing" else None,
                                html.H5(a['title'],className="press-title"),
                                html.H5(a['source'],className="press-source"),
                            ],
                        ),
                    dbc.CardBody(
                        [   dcc.Markdown(a['text']),
                            html.A(
                                href=a['website'],
                                className="stretched-link"
                            ),
                        ],
                    )
                ]

        card = dbc.Card(
                    card_content,
                    className="press-card h-100"
                )

        return dbc.Col(
                        [card],
                        style={"margin": "0.5rem"},
                        xs=12,
                        sm=12,
                        md=12,
                        lg=12,
                    )
    articles = \
        [
            dbc.Row(
                [
                    build_card(key_article[i]) for i in range(num_key_articles)
                ],
                justify="around",
            ),
            dbc.Row(dbc.Col(html.Hr())),
            dbc.Row(
                [
                    build_card(article[i]) for i in range(num_articles)
                ],
                justify="around",
            )
        ]

    body = dbc.Container(
            [
                dbc.Row([dbc.Col([html.H2("COVID Analytics in the Press"),])])
            ] + \
            articles,
            className="page-body"
        )


    layout = html.Div([nav, body, footer],className="site")
    return layout
