import dash_html_components as html
import dash_bootstrap_components as dbc
import yaml

from navbar import Navbar
from footer import Footer


def Collaborators():
    """Builds the AboutUs->Collaborators Page using assets/collaborators/organizations.yml"""

    with open("assets/collaborators/organizations.yml") as f:
        collaborators = yaml.load(f, Loader=yaml.FullLoader)

    def get_card(collab):
        return dbc.Col(
            style={"marginBottom": "32px"},
            xs=12, sm=6, md=4, xl=4,
            children=dbc.Card(
                style={"borderColor": "#800020"},
                className="h-100 collab-card",
                children=[
                    dbc.CardHeader(html.H4(collab["name"]), style={"textAlign": "center"}),
                    dbc.CardImg(
                        src='assets/collaborators/photos/%s' % collab['photo'],
                        top=False,
                        style={
                            "paddingLeft":   "20px",
                            "paddingRight":  "20px",
                            "paddingBottom": collab["padding"],
                            "paddingTop":    collab["padding"],
                        }
                    ),
                    dbc.CardFooter(
                        className="h-100",
                        children=[
                            html.A(
                                collab["text"],
                                href=collab["website"],
                                className="stretched-link collab-name"
                            ),
                        ],
                    )
                ],
            ),
        )
    body = dbc.Container(
        className="page-body",
        children=[
            dbc.Row(
                style={'marginBottom': 20},
                children=[
                    dbc.Col([
                        html.H2("Our Collaborators"),
                        html.P('Our models would not have been possible without the valuable data and insights \
                                provided by our partners. Our aspiration is to develop tools that they can positively \
                                affect the care they provide to their patients.')
                    ])
                ],
            ),
            dbc.Row([
                get_card(collaborators[i]) for i in range(len(collaborators))
            ]),
        ],
    )

    return html.Div([Navbar(), body, Footer()], className="site")
