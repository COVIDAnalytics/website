### Data
import datetime
import pandas as pd

### Graphing
import plotly.graph_objects as go
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from projections.projections import build_us_map
from assets.mappings import states

nav = Navbar()
footer = Footer()

def build_tom_us_map():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return build_us_map(tomorrow)


def build_card(imgTop,title,text,img,link):
    if imgTop:
        card_content = \
                [
                    dbc.CardImg(src=img, top=False),
                    dbc.CardBody(
                        [
                            html.H4(title, className="card-title"),
                            dcc.Markdown(text),
                            html.A(href=link,
                            className="stretched-link home-card"),
                        ],
                        className="home-card-body"
                    ),
                ]

    else:
        card_content = \
                [
                    dbc.CardBody(
                        [
                            html.H4(title, className="card-title"),
                            dcc.Markdown(text),
                            html.A(href=link,
                            className="stretched-link home-card"),
                        ],
                        className="home-card-body"
                    ),
                    dbc.CardImg(src=img, top=True),
                ]

    card = dbc.Card(
                card_content,
                className="home-card h-100"
            )

    return dbc.Col(
                    [card],
                    style={"margin": "0.5rem"},
                    xs=12,
                    sm=5,
                    md=5,
                    lg=2,
                )


data_text = '''
       130+ international Covid-19 clinical studies,
       aggregated into a single dataset.
       '''
insights_text = '''
      Key characteristics of COVID-19 patients in an
      interactive summary.
      '''
projections_text = '''
    State-by-state predictions of COVID-19 infections, \
    hospital stays, and deaths.
    '''

ventilator_text = '''
       Leveraging delays between state peaks to \
       optimally re-use ventilators.
       '''

calculator_text = '''
      Personalized calculator predicting mortality given hospitalization.
      '''

body = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Markdown(
                     '''
                     We are a group of researchers from the [MIT](http://mit.edu/) [Operations Research Center](https://orc.mit.edu/), \
                     led by Professor [Dimitris Bertsimas](https://www.mit.edu/~dbertsim/). \
                     We aim to quickly develop and deliver tools for hospitals and policymakers in the US to combat the spread of COVID-19. \
                     This work represents a collaborative effort with [Hartford HealthCare](https://hartfordhealthcare.org/) \
                     and [ASST Cremona](https://www.asst-cremona.it) which have been providing us with data and support through the model creation process.
                     '''
                ),
            ),
        ),
        dbc.Row(
            [
                build_card(True,"Data",data_text,"assets/images/data-1.jpg","/dataset"),
                build_card(False,"Insights",insights_text,"assets/images/insights-4.png","/interactive-graph"),
                build_card(True,"Projections",projections_text,"assets/images/forecast-1.png","/projections"),
                build_card(False,"Ventilator allocation",ventilator_text,"assets/images/allocation.png","/ventilator_allocation"),
                build_card(True,"Risk calculator",calculator_text,"assets/images/tree-2.png","/calculator"),
            ],
            justify="around",
            no_gutters=True,
        ),
        dbc.Row(
        [
            dbc.Col(
            [
              html.Div(
                  id = 'us_map_homepage',
                  children = build_tom_us_map(),
              ),
            ]
            )
        ],
        )
    ],
    className="page-body"
)

def Homepage():
    layout = html.Div([nav, body, footer], className="site")
    return layout
