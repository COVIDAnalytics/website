import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

def FinancialReliefPlanning():
    nav = Navbar()
    footer = Footer()

    body = dbc.Container(
            [
                dbc.Row(
                [
                    dbc.Col(
                    [
                        dbc.Jumbotron(
                        [
                            html.H2("Analytics-Driven Financial Relief Planning"),
                            dcc.Markdown(
                                 """The unemployment rate in the US has reached levels not seen since the Great Depression
                                    as millions of workers are out of work and trying to navigate difficult financial decisions.
                                    Households are struggling to figure out revised budgets, estimated cuts in spending, and
                                    potential resources to access additional funds. The decisions are complicated because
                                    there is an overwhelming number of COVID related benefits to understand, for example, the
                                    recent [CARES Act](https://home.treasury.gov/policy-issues/cares) and the
                                    [IRS Tax relief benefits](https://www.irs.gov/newsroom/coronavirus-related-relief-for-retirement-plans-and-iras-questions-and-answers).
                                 """,
                            ),
                            html.Hr(),
                            dcc.Markdown(
                                 """Although it is now easier to tap into retirement funds for short term budgeting needs,
                                    households need to evaluate overall tax consequences and long-term retirement plan goals
                                    to make the best decisions. It is very complicated to sort through all the information and
                                    options available. Analytics can help structure the information, define short and long-term
                                    household objectives, as well as incorporate personal constraints. Optimization techniques
                                    can be used to evaluate all possible decisions and determine the specific actions the
                                    household can take to navigate the current crisis and stay the course toward their future
                                    goals.
                                 """,
                            )
                        ],
                        style={'paddingBottom':'0.5rem','paddingTop':'0.8rem'}
                        )
                    ]
                    ),
                ],
                )
            ] + \
            [
                dbc.Row(
                [
                    dbc.Col(
                    [
                        dbc.Jumbotron(
                        [
                            html.H2("Financial Relief Planning Tool"),
                            dcc.Markdown(
                                 """A team of MIT PhDs from the Operations Research Center with 20+ years of experience in finance,
                                    analytics, and robust optimization have created the COVID Relief Planning Assistant to help those
                                    impacted create a short-term financial plan. This online tool leverages advanced analytics and
                                    modeling to tell households what to do next and why. There is no cost to access the tool
                                    which provides actionable financial guidance, personalized for each household impacted by
                                    reduced or lost income. The methodology of the tool is explained here.
                                 """,
                            ),
                            html.Hr(),
                            html.H5("COVID Relief Planning Assistant", style={"color":"#800020"}),
                            dcc.Markdown(
                                 """Click [here](https://covid.savvifi.com/) to get started on your short-term financial plan.
                                 """,
                            ),
                            html.H5("COVID Educational Resources"),
                            dcc.Markdown(
                                 """Click [here](https://help.savvifi.com/en/collections/2289225-covid-19-educational-resources)
                                    to find additional educational content for those affected by the COVID-19 crisis.
                                 """,
                            )
                        ],
                        style={'paddingBottom':'0.5rem','paddingTop':'0.8rem'}
                        )
                    ]
                    ),
                ],
                )
            ],
            className="page-body"
        )

    layout = html.Div([nav, body, footer], className="site")
    return layout
