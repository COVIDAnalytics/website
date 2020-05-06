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

from projections.visuals_funcs import build_continent_map
from projections.utils import world_map_text
from assets.mappings import states

nav = Navbar()
footer = Footer()

def build_tom_us_map():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return build_continent_map(tomorrow)


def build_card(imgTop,titles,text,img,links):
    cardbody = []
    for i,t in enumerate(titles):
        cardbody.append(html.A(t,href=links[i],className="card-title"))
        cardbody.append(dcc.Markdown(text[i]))


    if imgTop:
        card_content = \
                [
                    dbc.CardImg(src=img, top=False),
                    dbc.CardBody(
                        cardbody,
                        className="home-card-body"
                    ),
                ]

    else:
        card_content = \
                [
                    dbc.CardBody(
                        cardbody,
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
                )


data_text = '''
       130+ international Covid-19 clinical studies,
       aggregated into a single dataset.
       '''
insights_text = '''
    Key characteristics of COVID-19 patients in an
    interactive summary. '''

projections_text = '''
    Epidemiological predictions of COVID-19 \
    infections, hospital stays, and mortalities.
    '''

policy_text = '''
    Predicting infections and deaths based on various policy \
    implementations'''


ventilator_text = '''
       Leveraging delays between state peaks to \
       optimally re-use ventilators.
       '''

mortality_calculator_text = '''
      Personalized calculator predicting mortality upon hospitalization.
      '''

infection_calculator_text = '''
    Personalized calculator predicting results of COVID test.
    '''

cards = \
    [
        {
            "titles": ["Data","Insights"],
            "text": [data_text,insights_text],
            "image": "assets/images/insights-4.png",
            "links": ["/dataset","/interactive-graph"]
        },
        {
            "titles": ["Infection risk calculator","Mortality risk calculator"],
            "text": [infection_calculator_text,mortality_calculator_text],
            "image": "assets/images/infection_logo.jpg",
            "links": ["/infection_calculator","/mortality_calculator"]
        },
        {
            "titles": ["Case predictions","Policy Evaluations"],
            "text": [projections_text,policy_text],
            "image": "assets/images/forecast-1.png",
            "links": ["/projections","/policies"]
        },
        {
            "titles": ["Ventilator allocation"],
            "text": [ventilator_text],
            "image": "assets/images/allocation.png",
            "links": ["/ventilator_allocation"]
        }

    ]


body = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Markdown(
                     '''
                     We are a group of researchers from the [MIT](http://mit.edu/) [Operations Research Center](https://orc.mit.edu/), \
                     led by Professor [Dimitris Bertsimas](https://www.mit.edu/~dbertsim/). \
                     We aim to quickly develop and deliver tools for hospitals and policymakers in the US to combat the spread of COVID-19. \
                     This work represents a collaborative effort with [multiple hospitals](/collaborators) which have been providing us with \
                     data and support throughout the model creation process.
                     '''
                ),
            ),
        ),
        dbc.Row(
            [
                build_card(False,cards[0]["titles"],cards[0]["text"],cards[0]["image"],cards[0]["links"]),
                build_card(True,cards[1]["titles"],cards[1]["text"],cards[1]["image"],cards[1]["links"]),
                build_card(False,cards[2]["titles"],cards[2]["text"],cards[2]["image"],cards[2]["links"]),
                build_card(True,cards[3]["titles"],cards[3]["text"],cards[3]["image"],cards[3]["links"]),

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
              html.P(
                      children = world_map_text,
                      style={'color':'gray'},
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
