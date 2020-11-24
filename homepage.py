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
from projections.utils import get_world_map_text

def Homepage():

    nav = Navbar()
    footer = Footer()

    def build_tom_us_map():
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates = ['Day'])
        df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
        df_projections = df_projections.loc[df_projections['Day']==tomorrow]
        pop_info = pd.read_csv('data/predicted/WorldPopulationInformation.csv', sep=",")
        return build_continent_map(df_projections,pop_info,tomorrow)

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

    treatments_calculator_text = '''
        Personalized recommendations of ACEI/ARB prescriptions for hypertensive patients.
        '''

    financial_text =  '''
        Unemployment is rising. How analytics can help inform COVID-19 related financial decisions.
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
                "titles": ["Treatment prescriptions","Mortality risk calculator"],
                "text": [treatments_calculator_text,mortality_calculator_text],
                "image": "assets/images/infection_logo.jpg",
                "links": ["/treatments","/mortality_calculator"]
            },
            {
                "titles": ["Case predictions","Policy evaluations"],
                "text": [projections_text,policy_text],
                "image": "assets/images/forecast-1.png",
                "links": ["/projections","/policies"]
            },
            {
                "titles": ["Ventilator allocation"],
                "text": [ventilator_text],
                "image": "assets/images/allocation.png",
                "links": ["/ventilator_allocation"]
            },
            {
                "titles": ["Financial relief planning"],
                "text": [financial_text],
                "image": "assets/images/financial_logo.jpeg",
                "links": ["/financial_relief","/interactive-graph"]
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
                    build_card(False,cards[4]["titles"],cards[4]["text"],cards[4]["image"],cards[4]["links"]),
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
                          children = get_world_map_text(),
                          style={'color':'gray'},
                  ),
                ]
                )
            ],
            )
        ],
        className="page-body"
    )

    layout = html.Div([nav, body, footer], className="site")
    return layout
