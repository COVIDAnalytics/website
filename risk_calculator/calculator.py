import pickle
import plotly.graph_objects as go
from textwrap import wrap

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.features import build_feature_cards,features

nav = Navbar()
footer = Footer()

with open('assets/risk_calculators/rf_model.pkl', 'rb') as file:
    model = pickle.load(file)

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
              html.H2("Clinical Rick Calculator")
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                [
                    dcc.Markdown(
                         """Severe COVID-19 patients require our most limited health care resources,\
                          ventilators and intensive care beds. As a result, physicians have the hard \
                          responsibility to decide which patients should have priority access to these \
                          resources. To help them make an informed decision, we construct and publish \
                          patient risk calculators tailored for COVID-19 patients.
                         """,
                    ),
                    dcc.Markdown(
                         """ **Disclaimer:** A model is only as good as the data it is trained on. We will \
                         release new versions of the calculator as the amount of data we receive from \
                         our partner institutions increases. If you are a medical institution and are \
                         willing to contribute to our effort, feel free to reach out to us [here](/contact).
                         """,
                    ),
                    dcc.Markdown(
                         """ **Data** (as of 2020/04/10): Our model is trained on 496 patients from the Azienda \
                         Socio-Sanitaria Territoriale di Cremona [ASST Cremona](https://www.asst-cremona.it/) which includes the Ospedale \
                         di Cremona, Ospedale Oglio Po and other minor public hospitals in the Province of \
                         Cremona. Cremona is one of the most hit italian provinces in Lombardy in the Italian \
                         COVID-19 crisis with a total of several thousand positive cases to date. Given our training \
                         population, we are most confident about the relevance of our model to: (a) Western population; \
                         (b) Severe to acute patients; (c) Congested hospitals. \
                         """,
                    ),
                    dcc.Markdown(
                         """ **This is a developmental version. It is not intended for patient or clinician use.\
                          It is available only to solicit input about its future development.**
                         """,
                         ),
                ]
                )
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
                html.H5('Insert the features below into the risk calculator.')
            ),
        ]),
        dbc.Row(build_feature_cards(),justify="center"),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Submit",
                    id="submit-features-calc",
                    n_clicks=0,
                    className="mr-1"
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                dcc.ConfirmDialog(
                    id='calc-input-error',
                ),
                dbc.Card(
                    [
                        dbc.CardBody(id="score-calculator-card-body")
                    ],
                    color="dark",
                    inverse=True,
                    style={"marginTop":20,"marginBottom":20}
                    ),
                ],
                xs=12,
                sm=6,
                md=6,
                lg=3,
            ),
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        id = 'feature-importance-bar-graph',
                        children = [],
                    )
                ],
            ),
            justify="center",
        ),
    ],
    className="page-body"
)

def RickCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input(feature_vals):
    numeric = len(features["numeric"])
    for feat in range(numeric):
        val = feature_vals[feat]
        content = features["numeric"][feat]
        name = content["name"]
        min_val = content["min_val"]
        max_val = content["max_val"]
        if val is None:
            return False, "Please insert a numeric value for {}".format(name)
        if val < min_val or val > max_val:
            return False, "Please insert a numeric value for {} between {} and {}".format(name,min_val,max_val)
    return True,""

def predict_risk(feature_vals):
    x = [0]*len(model.feature_importances_)
    i = 0
    for feat in features["numeric"]:
        x[feat["index"]] = feature_vals[i]
        i+=1
    for feat in features["categorical"]:
        x[feat["index"]] = feature_vals[i]
        i+=1
    symptoms = feature_vals[i]
    comorbidities = feature_vals[i+1]
    for s in symptoms:
        ind = features["checkboxes"][0]["vals"].index(s)
        x[ind] = 1
    for c in comorbidities:
        ind = features["multidrop"][0]["vals"].index(c)
        x[ind] = 1
    score = model.predict_proba([x])[:,1]
    score = round(1 - score[0], 2)
    card_content = [
        html.H4("The mortality risk score is:",className="score-calculator-card-content"),
        html.H4(score,className="score-calculator-card-content"),
    ]
    return card_content

def build_feature_importance_graph():
    feature_list = ['']*len(model.feature_importances_)
    i = 0
    for feat in features["numeric"]:
        feature_list[feat["index"]] = feat["name"]
        i+=1
    for feat in features["categorical"]:
        feature_list[feat["index"]] = feat["name"]
        i+=1
    for feat in features["checkboxes"]:
        for j,name in enumerate(feat["vals"]):
            feature_list[feat["index"][j]] = name
            i+=1
    for feat in features["multidrop"]:
        for j,name in enumerate(feat["vals"]):
            feature_list[feat["index"][j]] = name
            i+=1
    importances = list(model.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)[:10]
    x,y = zip(*feature_importances)
    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color="#800020"))])
    graph = dcc.Graph(
        id='feature-importance-graph',
        figure=fig,
    )

    fig.update_layout(
                height=550,
                title={
                    'text':'<br>'.join(wrap('<b> Feature Importances (Top 10) </b>', width=26)) ,
                     'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Features",'linecolor': 'lightgrey'},
                yaxis={'title': "Importance",'linecolor': 'lightgrey'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )
    return graph
