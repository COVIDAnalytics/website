import dash_html_components as html
import dash_bootstrap_components as dbc
import yaml

from navbar import Navbar
from footer import Footer

def Collaborators():
    with open("assets/collaborators/organizations.yml") as f:
        collaborators = yaml.load(f, Loader=yaml.FullLoader)
    num_collaborators = len(collaborators)

    nav = Navbar()
    footer = Footer()

    def get_card(collab):
        return \
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H4(collab["name"]),style={"textAlign": "center"}),
                        dbc.CardImg(src='assets/collaborators/photos/%s' % collab['photo'],
                                    top=False,
                                    style={"paddingLeft":   "10px",
                                           "paddingRight":  "10px",
                                           "paddingBottom": collab["padding"],
                                           "paddingTop":    collab["padding"],}),
                        dbc.CardFooter(
                            [
                                html.A(collab["text"],
                                href=collab["website"],
                                className="stretched-link collab-name"),
                            ],
                            className="h-100",
                        )
                    ],
                    style={"borderColor": "#800020"},
                    className="h-100 collab-card"
                ),
                xs=12,
                sm=6,
                md=3,
                lg=3,
                xl=3,
                style={"padding": "20px"},
            )

    body = dbc.Container(
        [   dbc.Row(
                    [
                        dbc.Col(
                        [
                            html.H2("Our Collaborators"),
                            html.P('Our models would not have been possible without the valuable data and insights provided \
                                    by our partners. Our aspiration is to develop tools that they can positively affect the \
                                    care they provide to their patients.')
                        ]
                        )
                    ],
                    style={'marginBottom': 20}
                ),
            dbc.Row(
                [
                    get_card(collaborators[i]) for i in range(num_collaborators)
                ],
            ),
        ],
       className="page-body"
    )
    layout = html.Div([nav, body, footer],className="site")
    return layout
