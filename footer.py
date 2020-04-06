import dash_html_components as html
import dash_bootstrap_components as dbc

def Footer():
    footer = html.Footer(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(src="assets/logo_black.png", height="70px")
                            ],
                        ),
                        dbc.Col(
                            html.A(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Img(src="assets/mit.png", height="60px")),
                                            dbc.Col(html.Img(src="assets/orc.png", height="50px")),
                                        ],
                                        no_gutters=True,
                                    ),
                                    href="https://orc.mit.edu/",
                                 ),
                        ),
                        dbc.Col(
                            [
                                dbc.NavLink("Team", href="/team", style={"font-size":15,"margin-right":10}),
                                dbc.NavLink("Contact Us", href="/contact", style={"font-size":15,"margin-bottom":0}),
                            ],
                        ),
                    ],
                ),
                id="footer",
            )

    return footer
