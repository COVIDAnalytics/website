import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

from projections.map import get_top_visual, build_death_cards
from projections.timeline import get_bottom_visual
from projections.utils import build_notes_content


def ProjectState():
    nav = Navbar()
    footer = Footer()

    body = dbc.Container(
        className="page-body",
        children=[
            dcc.Store(id='sync', data='US'),
            dbc.Row([
                dbc.Col(
                    lg=12,
                    style={"marginBottom": "20px"},
                    children=[html.H2("DELPHI Epidemiological Case Predictions")],
                ),
                dbc.Col(
                    lg=12,
                    children=build_notes_content(),
                ),
                dbc.Col(
                    xs=12,
                    sm=12,
                    md=12,
                    xl=6,
                    lg=5,
                    style={"marginBottom": "30px"},
                    children=[
                        html.Div(** {"data-aos": "fade-up"}, className="aos-refresh-onload-strict", children=dbc.Card(
                            className="elevation-3",
                            style={"padding": "30px", "border": "none", "height": "100%", "backgroundColor": "#e9ecef"},
                            children=[
                                dcc.Markdown("""\
                                               A critical tool for COVID-19 planning is charting out the progression \
                                               of the pandemic across the United States and the world. \
                                               We've developed a new epidemiological model called DELPHI, which \
                                               forecasts infections, hospitalizations, and deaths. \
                                               You can think of our model as a standard \
                                               [SEIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model) \
                                               with additional \
                                               features specific to the COVID-19 pandemic, like under-detection and \
                                               differentiated government intervention.
                                       """, style={"marginTop": "auto"}),
                                dbc.Button(children=["Expand notes",
                                                     html.Span("chevron_right", className="material-icons",
                                                               style={"margin": "0px"})],
                                           id="projection-show-notes-btn", color="dark",
                                           style={"borderRadius": "0px",
                                                  "maxWidth": "170px",
                                                  "marginBottom": "1rem",
                                                  "display": "flex",
                                                  "backgroundColor": "#A31F34",
                                                  "border": "none",
                                                  "justifyContent": "space-evenly"}),
                                dcc.Markdown('''If you want to learn more, view our \
                                            [documentation](/projections_documentation) or \
                                            [source code](https://github.com/COVIDAnalytics/epidemic-model).'''),
                            ]),
                        )
                    ],
                ),
                dbc.Col(
                    lg=7,
                    xl=6,
                    style={"marginTop": "auto"},
                    children=build_death_cards()),

            ])
        ] + get_top_visual() + get_bottom_visual(),
    )

    layout = html.Div([nav, body, footer], className="site")
    return layout
