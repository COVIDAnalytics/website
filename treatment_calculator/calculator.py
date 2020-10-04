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
        [dcc.Tabs(
            id="treatments-calc-tabs",
            children=[
                dcc.Tab(
                    label='Inputs',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                        html.Div(
                            style={"min-height": "550px"},
                            children=
                                build_row_header("Treatment Selection") + [
                                    dbc.Row(
                                        justify="center",
                                        style={"marginBottom": "40px", "marginTop": "40px"},
                                        children=dbc.Col(
                                        xs=12,
                                        sm=12,
                                        md=8,
                                        lg=6,
                                        children=
                                            dcc.Dropdown(
                                                id="treatments-sel",
                                                value=0,
                                                options=[{"label": treatments[x], "value": x}
                                                         for x in range(len(treatments))]),
                                    ))
                                ] +
                                build_row_header("Patient Information") + [
                                dbc.Row(
                                    id="treatments-calc-feature-cards",
                                    justify="center"
                                ),
                                dbc.Row(
                                    justify="center",
                                    children=dbc.Col(
                                        xl=4,
                                        lg=4,
                                        md=8,
                                        sm=12,
                                        children=[
                                            dbc.Button(
                                                id="submit-treatments-calc",
                                                style={"width": "100%", "height": 120},
                                                color="danger",
                                                children=[
                                                html.H5("Submit", style={
                                                    "color": "white",
                                                    "fontSize": 35
                                                }),
                                            ])
                                        ]
                                    )
                                )
                            ]
                        )
                    ]
                ),
                dcc.Tab(
                    label='Results',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
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

