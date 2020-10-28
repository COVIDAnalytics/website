import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from navbar import Navbar
from footer import Footer
from risk_calculator.visuals import get_lang
from treatment_calculator.utils import treatments, get_jumbo_text


def build_row_header(name):
    return [dbc.Row(
        justify="start",
        style={
            "marginBottom": "20px",
        },
        children=dbc.Col(
            dbc.Card(
                className="elevation-3 treatments-header",
                children=html.H3(name)
            )
        )
    )]

def TreatmentCalc():
    nav = Navbar()
    footer = Footer()
    body = dbc.Container(
        className="page-body",
        children=
        #get_lang("treatments-calc-language") +
        [
            dbc.Row(
                children=[
                    dbc.Col([
                        html.Div(
                            **{"data-aos": "fade-up"},
                            className="aos-refresh-onload",
                            children=dbc.Jumbotron(
                                style={"padding": "4%"},
                                className="elevation-3",
                                children=get_jumbo_text()
                            )
                        )
                    ]),
                ]
            )
        ] +
        [dcc.Tabs(
            id="treatments-calc-tabs",
            children=[
                dcc.Tab(
                    label='Patient Information',
                    value='tab-1',
                    className='treatments-tab',
                    selected_className='treatments-tab--selected',
                    children=[
                        html.Div(
                            style={"min-height": "550px"},
                            children=[
                                dbc.Row(
                                    id="treatments-calc-feature-cards",
                                    justify="center"
                                ),
                                dbc.Row(
                                    justify="center",
                                    children=[
                                        dbc.Col(
                                            xl=4,
                                            lg=4,
                                            md=8,
                                            sm=12,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardBody([
                                                            html.H5("Recommend treating if it yields a",
                                                                    style={"color": "grey"}),
                                                            dbc.Row([
                                                                dbc.Input(id="treatments-thresh",
                                                                    type="number",
                                                                    style={"textAlign": "center", "maxWidth": 80},
                                                                    value="1"),
                                                                html.H5("% improvement",
                                                                        style={"color": "grey", "lineHeight": "33px",
                                                                               "marginLeft": "10px"})
                                                            ], no_gutters=True)
                                                        ])
                                                    ]
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            xl=4,
                                            lg=4,
                                            md=8,
                                            sm=12,
                                            children=[
                                                dbc.Button(
                                                    id="submit-treatments-calc",
                                                    style={"width": "100%", "height": "100%"},
                                                    color="danger",
                                                    children=[
                                                    html.H5("Submit", style={
                                                        "display": "inline",
                                                        "color": "white",
                                                        "fontSize": 35,
                                                        "verticalAlign": "top"
                                                    }),
                                                    html.H5("", className="material-icons", style={
                                                        "display": "inline",
                                                        "color": "white",
                                                        "fontSize": 40,
                                                        "fontWeight": "800",
                                                        "verticalAlign": "bottom"
                                                    })
                                                ])
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        dcc.Loading(
                            type="graph",
                            fullscreen=True,
                            # hacky. trigger loading whenever treamtnets-reuslts graph changes
                            children=html.Div(id="treatments-results-graph")
                        ),
                    ]
                ),
                dcc.Tab(
                    label='Results',
                    value='tab-2',
                    className='treatments-tab',
                    selected_className='treatments-tab--selected',
                    children=[
                        html.Div(id="treatments-results-graph"),
                    ]
                ),
            ]
        )] +
        [html.Div(style={"height": "100px"})]
    )
    layout = html.Div([nav, body, footer], className="site")
    return layout

