import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from navbar import Navbar
from footer import Footer
from risk_calculator.visuals import get_lang
from treatment_calculator.utils import treatments


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
        get_lang("treatments-calc-language") +
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
                                children=[
                                    html.H2("Evaluating ACEI / ARBS Treatments"),
                                    html.Hr(),
                                    dcc.Markdown(
                                        """
                                        This tool uses various machine learning models to evaluate a patient's risk 
                                        on undertaking COVID-19 treatment. Based on these results... Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged
                                        """,
                                    ),
                                ]
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
                                                            html.H5("Recommend treating if it yields a", style={"color": "grey"}),
                                                            dbc.Input(id="treatments-thresh", type="number", placeholder="1% improvement to mortality rate"),
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
                        )
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

