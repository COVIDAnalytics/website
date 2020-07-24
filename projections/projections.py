import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

from projections.map import get_top_visual, build_death_cards
from projections.timeline import get_bottom_visual

def ProjectState():
    nav = Navbar()
    footer = Footer()

    body = dbc.Container(
        className="page-body",
        children=[dbc.Row([
            dbc.Col(
                xs=12,
                sm=12,
                md=12,
                lg=7,
                children=[
                    html.H2("DELPHI Epidemiological Case Predictions"),
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
                    """),
                    dcc.Markdown('''If you want to learn more, check out the \
                         [documentation](/projections_documentation) or \
                         [source code](https://github.com/COVIDAnalytics/epidemic-model).'''),
                    dcc.Markdown('''**Note: The model has been updated on 7/4/2020 to better reflect the resurgence of \
                         cases in various locations. The projections could differ significantly from previous results in certain areas.** '''),
                    dbc.Card(
                        className='projections-general-card',
                        children=[dbc.CardBody([
                            html.H5("Note: what do we mean by \"active cases\"?"),
                            dcc.Markdown("We define a COVID-19 case as **active** \
                                 if it has not yet resulted in recovery \
                                 or death. You may notice a discrepancy \
                                 between the number of active cases here \
                                 and on the \
                                 [JHU map](https://coronavirus.jhu.edu/map.html). \
                                 The JHU map is very good at keeping track of new cases, \
                                 but does not always publish data on recovered cases, \
                                 which can lead to overestimating currently active \
                                 cases."),
                            dcc.Markdown("**Disclaimer:** Our total counts only account for \
                                 countries in which we have sufficient data and where \
                                 the pandemic is currently active. In particular, it \
                                 excludes some East Asian countries where the pandemic \
                                 has largely passed.\n \
                                 \nCountry-level projections are modelled based on all \
                                 historical data to increase the accuracy of future \
                                 predictions. As such, daily counts extracted from \
                                 the model may not exactly correspond with reports."),
                        ])],
                    ),
                ]
            ),
            dbc.Col(build_death_cards())
        ])
        ] + \
            get_top_visual() + \
            get_bottom_visual(),
    )

    layout = html.Div([nav, body, footer], className="site")
    return layout
