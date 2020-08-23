import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from navbar import Navbar
from footer import Footer
from risk_calculator.visuals import get_lang


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
                    label='Tab one',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
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
                                    children=dbc.Col(
                                        xl=4,
                                        lg=4,
                                        md=8,
                                        sm=12,
                                        children=[
                                            dbc.Button(
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
                    label='Tab two',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
            ]
        )] +
        [html.Div(style={"height": "100px"})]
    )
    layout = html.Div([nav, body, footer], className="site")
    return layout

