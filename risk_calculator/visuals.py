import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from .utils import lang_names


def get_page_desc(_id):
    """Builds the first big text card that introduces users to the page"""
    return [
        dbc.Row([
            dbc.Col([
                dbc.Jumbotron(
                    id=_id,
                    style={'paddingBottom': '0.5rem', 'paddingTop': '0.8rem'}
                )
            ]),
        ])
    ]


def get_labs_indicator(_id, instructions_id):
    """This is the card where user selects if he has lab values or not"""
    return [
        dbc.Row(
            justify="center",
            align="stretch",
            children=[
                dbc.Col(
                    xs=12, sm=12, md=12, lg=6,
                    children=html.Div(
                        **{"data-aos": "fade-up", "data-aos-delay": "0"},
                        style={"transformStyle": "flat", "zIndex": "50"},
                        children=dbc.Card(
                            style={"borderWidth": "0px",
                                   "height": "125px",
                                   "marginBottom": 30},
                            className="elevation-3",
                            children=[
                                dbc.CardHeader(id=_id + "_text",
                                               style={"fontWeight": "bold"}),
                                dbc.CardBody([
                                   dbc.Row([
                                        dbc.Col(
                                            html.Div([
                                                dcc.Dropdown(
                                                    clearable=False,
                                                    id=_id,
                                                    value=0,
                                                    className="dcc_dropdown",
                                                ),
                                            ]),
                                        ),
                                    ]),
                                ]),
                            ]
                        ),
                    )
                ),
                dbc.Col(
                    xs=12, sm=12, md=12, lg=6,
                    children=html.Div(
                        **{"data-aos": "fade-up", "data-aos-delay": "100"},
                        children=dbc.Card(
                            className="elevation-3",
                            style={"borderWidth": "0px", "height": "125px", "marginBottom": 30},
                            children=[
                                dbc.CardBody([
                                    # The headline that says 'insert the features below'
                                    dbc.Row(
                                        justify="center",
                                        style={"height": "100%", "padding": 2, "opacity": "0.6"},
                                        no_gutters=True,
                                        children=[
                                            dbc.Col(
                                                style={"flexGrow": "0"},
                                                align="center",
                                                children=html.Div(
                                                    className="material-icons",
                                                    children="info",
                                                    style={"fontSize": "40px", "paddingRight": 20}
                                                ),
                                            ),
                                            dbc.Col(
                                                align="center",
                                                children=html.H5(
                                                    id=instructions_id,
                                                    style={"fontSize": "18px"}
                                                ),
                                            )
                                        ]
                                    ),
                                ]),
                            ]
                        ),
                    )
                )
            ]
        ),
    ]


def get_model_desc(id):
    """This is the big text card that has the technical details of the model"""
    return [
        dbc.Row(
            justify="center",
            children=dbc.Jumbotron(
                id=id,
                style={'paddingBottom': '0.5rem', 'paddingTop': '0.8rem'}
            ),
        ),
    ]


def get_feature_importance(_id):
    """This is the card that houses the feature importance graph at the bottom of the page"""
    return [
        dbc.Row(
            justify="center",
            children=dbc.Col([
                dbc.Card(
                    id=_id,
                    style={"borderColor": "#800020", "paddingTop": 20, "paddingBottom": 20},
                ),
            ]),
        ),
    ]


def get_feature_cards(_id):
    """Create feature card container"""
    return [
        # The container of feature cards
        dbc.Row(
            id=_id,
            justify="center"
        )
    ]


def get_submit_button(_id, res_id, err_id, imputed_id):
    """Build submit button"""
    return [
        dbc.Row(
            justify="center",
            style={"paddingBottom": 50},
            children=[
                dbc.Col(
                    xs=12,
                    sm=4,
                    md=4,
                    lg=4,
                    style={"paddingBottom": 20},
                    children=html.Div(
                        **{"data-aos": "fade-up"},
                        id="submit-features-calc-wrapper",
                        className="aos-refresh-onload",
                        children=dbc.Button(
                            id=_id,
                            n_clicks=0,
                            className="mr-1 calc-submit-button elevation-3"
                        ),
                    )
                ),
                # The card that shows the user's score
                dbc.Col(
                    xs=12,
                    sm=8,
                    md=8,
                    lg=8,
                    style={"paddingBottom": 20},
                    children=html.Div(
                        **{"data-aos": "fade-up", "data-aos-delay": "100"},
                        className="aos-refresh-onload",
                        id=res_id
                    )
                ),
                dbc.Col(
                    xs=12, sm=12, md=12, lg=12,
                    children=html.P(
                        id=err_id,
                        style={"color": "red", "textAlign": "center"}
                    ),
                ),
                dbc.Col(
                    xs=12, sm=12, md=12, lg=12,
                    children=dcc.Markdown(id=imputed_id)
                ),
            ],
        ),
    ]


def get_results_card(_id, err_id):
    """Build score card and error message text"""
    return [
    ]


def get_inputed_vals(_id):
    """Build the text that says what values where imputed"""
    return [
    ]


def get_personal_visual(_id):
    """Builds the user's personal visual that shows feature contribution to risk score"""
    return [
        dbc.Row(
            justify="center",
            children=dbc.Col([
                dbc.Card(
                    style={
                        "borderColor": "white",
                    },
                    children=[
                        dcc.Markdown(
                            id=_id + "-explanation"
                        ),
                        html.Img(
                            id=_id,
                            style={"height": 200}
                        ),
                    ]
                )
            ]),
        ),
    ]


def get_lang(_id):
    """Builds the language selection dropdown at the top of the page"""
    return [
        dbc.Row(
            justify="end",
            children=dbc.Col(
                xs=5, sm=5, md=4, lg=3,
                children=html.Div(
                    dcc.Dropdown(
                        id=_id,
                        clearable=False,
                        options=list(sorted([{'label': lang_names[x], 'value': x} for x in range(len(lang_names))],
                                            key=lambda i: i['label'])),
                        value=0,
                        style={'marginBottom': 10, "width": "100%"},
                        className="dcc_dropdown",
                    ),
                ),
            ),
        ),
    ]


