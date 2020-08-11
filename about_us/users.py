import dash_html_components as html
import dash_bootstrap_components as dbc
import yaml

from navbar import Navbar
from footer import Footer


def Users():
    """Builds the AboutUs->Model Users using assets/users/organizations.yml"""

    with open("assets/users/organizations.yml") as f:
        collaborators = yaml.load(f, Loader=yaml.FullLoader)
        collaborators = list(sorted(collaborators, key=lambda i: i["name"]))

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
                        src='assets/users/photos/%s' % collab['photo'],
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
                        html.H2("Model Users"),
                        html.P('Listed here are organizations who use our models. **EDIT ME**.')
                    ])
                ],
            ),
            dbc.Row([
                get_card(collaborators[i]) for i in range(len(collaborators))
            ]),
        ],
    )

    return html.Div([Navbar(), body, Footer()], className="site")
