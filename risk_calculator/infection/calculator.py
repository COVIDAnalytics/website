import pickle
import sklearn
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.features import build_feature_cards,features
from risk_calculator.utils import convert_temp_units

nav = Navbar()
footer = Footer()

with open('assets/risk_calculators/infection/positivity_with_lab.pkl', 'rb') as file:
    labs = pickle.load(file)

with open('assets/risk_calculators/infection/positivity_without_lab.pkl', 'rb') as file:
    no_labs = pickle.load(file)

labs_model = labs["model"]
labs_impoter = labs["imputer"]
labs_features = labs["json"]

no_labs_model = labs["model"]
no_labs_imputer = labs["imputer"]
no_labs_features = labs["json"]

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
              html.H2("Infection Risk Calculator")
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
                         """blah
                         """,
                    ),
                    dcc.Markdown(
                         """ **Disclaimer:** blah
                         """,
                    ),
                    dcc.Markdown(
                         """ **Data** blah \
                         """,
                    ),
                    dcc.Markdown(
                         """ **This is a developmental version. It is not intended for patient or clinician use.\
                          It is available only to solicit input about its future development.**
                         """,
                         )
                ]
                )
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dcc.Markdown("Do you have lab values?"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                [
                                                dcc.Dropdown(
                                                        id = 'lab_values_indicator_infection',
                                                        options = [{'label': x, 'value': x} for x in ["Yes","No"]],
                                                        value = 'No',
                                                ),

                                            ]),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                    className="projections-general-card h-100"
                ),
            ],
            justify="center",
            xs=12,
            sm=12,
            md=6,
            lg=6,
            ),
        ]
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                    id = 'infection-model-desc'
                )
            ],
            ),
        ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        id = 'feature-importance-bar-graph-infection',
                        style={"paddingTop":20,"paddingBottom":20}
                    )
                ],
            ),
            justify="center",
        ),
        dbc.Row(
        [
            dbc.Col(
                html.H5('Insert the features below into the risk calculator.')
            ),
        ]),
        dbc.Row(
                dbc.Col(
                    html.Div(
                        id = 'features-infection',
                    )
                )
            justify="center"
            ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    dbc.Button(
                        "Submit",
                        id="submit-features-calc-infection",
                        n_clicks=0,
                        className="mr-1"
                    ),
                id="submit-features-calc-wrapper",
                )
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                dcc.ConfirmDialog(
                    id='calc-input-error-infection',
                ),
                dbc.Card(
                    [
                        dbc.CardBody(id="score-calculator-card-body-infection")
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
    ],
    className="page-body"
)

def InfectionRickCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input_infec(labs,feature_vals):
    if labs == "No":
        features = no_labs_model
        imputer = no_labs_imputer
    else:
        features = labs_model
        imputer = labs_imputer
    numeric = len(features["numeric"])
    indexes = [0] * len(feature_vals)
    for feat in range(numeric):
        val = feature_vals[feat]
        if val is None:
            feature_vals[feat] = np.nan
            indexes[feat] = 1
        else:
            content = features["numeric"][feat]
            name = content["name"]
            min_val = content["min_val"]
            max_val = content["max_val"]
            if val < min_val or val > max_val:
                return False, "Please insert a numeric value for {} between {} and {}".format(name,min_val,max_val)
    res = imputer.transform(feature_vals)
    return True,"",res,np.multiply(indexes,res)

#  TODO immplement the logic in this function with missing and predict from xgboost
def predict_risk_infec(labs,feature_vals,missing):
    if labs == "No":
        model = no_labs_model
        features = no_labs_model
    else:
        model = labs_model
        features = labs_model
    x = [0]*len(model.feature_importances_)
    #if temperature is in F, switch measurement to Celsius
    convert_temperature = feature_vals[-1] == "°F"
    #align order of feature vector so that values are in correct order
    i = 0
    for feat in features["numeric"]:
        if feat["name"] == "Body Temperature" and convert_temperature:
            x[feat["index"]] = convert_temp_units(feature_vals[i])
        else:
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
    score = str(int(100*round(1 - score[0], 2)))+"%"
    card_content = [
        html.H4("The mortality risk score is:",className="score-calculator-card-content"),
        html.H4(score,className="score-calculator-card-content"),
    ]
    return card_content
