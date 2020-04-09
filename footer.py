import dash_html_components as html
import dash_bootstrap_components as dbc

def Footer():
    footer = html.Footer(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(src="assets/images/logo_black.png", height="70px")
                            ],
                        ),
                        dbc.Col(
                            html.A(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Img(src="assets/images/mit.png", height="60px")),
                                            dbc.Col(html.Img(src="assets/images/orc.png", height="70px")),
                                        ],
                                        no_gutters=True,
                                    ),
                                    href="https://orc.mit.edu/",
                                 ),
                        ),
                        dbc.Col(
                            html.Div([
                                html.A([
                                        html.Img(
                                            src='assets/images/icons/github.png',
                                            style={
                                                'height' : '15%',
                                                'width' : '15%',
                                                'position' : 'relative',
                                                'padding-top' : 0,
                                                'padding-right' : 0
                                            }
                                        )
                                ], href='https://github.com/COVIDAnalytics'),
                                html.A([
                                        html.Img(
                                            src='assets/images/icons/email.png',
                                            style={
                                                'height' : '15%',
                                                'width' : '15%',
                                                'position' : 'relative',
                                                'padding-top' : 0,
                                                'padding-right' : 0
                                            }
                                        )
                                ], href='/contact'),
                                html.A([
                                        html.Img(
                                            src='assets/images/icons/twitter.png',
                                            style={
                                                'height' : '15%',
                                                'width' : '15%',
                                                'position' : 'relative',
                                                'padding-top' : 0,
                                                'padding-right' : 0
                                            }
                                        )
                                ], href='https://twitter.com/covid_analytics'),
                            ])
                        ),
                    ],
                ),
                id="footer",
            )

    return footer
