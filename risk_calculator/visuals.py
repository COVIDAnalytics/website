import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from .utils import lang_names


def get_labs_indicator(_id):
    """This is the card where user selects if he has lab values or not"""
    return [
        dbc.Row(
            justify="center",
            children=dbc.Col(
                xs=12, sm=12, md=12, lg=9,
                children=dbc.Card(
                    style={"border-width": "0px"},
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
            ),
        )
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
        # The headline that says 'insert the features below'
        dbc.Row(
            justify="center",
            style={"padding": 50, "opacity": "0.8"},
            children=[
                html.Div(
                    id=_id + "-text",
                ),
            ]
        ),
        # The container of feature cards
        dbc.Row(
            id=_id,
            justify="center"
        )
    ]


def get_submit_button(_id):
    """Build submit button"""
    return [
        dbc.Row(
            style={"paddingBottom": 10},
            children=dbc.Col(
                html.Div(
                    id="submit-features-calc-wrapper",
                    children=dbc.Button(
                        id=_id,
                        n_clicks=0,
                        className="mr-1"
                    ),
                )
            ),
        ),
    ]


def get_results_card(_id, err_id):
    """Build score card and error message text"""
    return [
        # The red error text below the submit button
        dbc.Row(
            justify="center",
            children=dbc.Col(
                xs=12, sm=12, md=12, lg=12,
                children=html.P(
                    id=err_id,
                    style={"color": "red", "textAlign": "center"}
                ),
            ),
        ),
        # The card that shows the user's score
        dbc.Row(
            justify="center",
            children=dbc.Col(
                xs=12, sm=6, md=6, lg=3,
                children=dbc.Card(
                    color="dark",
                    inverse=True,
                    style={"marginTop": 10, "marginBottom": 20},
                    children=dbc.CardBody(id=_id)
                ),
            ),
        ),
    ]


def get_inputed_vals(_id):
    """Build the text that says what values where imputed"""
    return [
        dbc.Row(
            justify="center",
            children=dbc.Col([
                dcc.Markdown(
                    id=_id
                )
            ]),
        )
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
