import pickle

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import convert_temp_units, predict_risk, valid_input
from risk_calculator.visuals import get_labs_indicator,get_model_desc,get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_feature_cards, get_submit_button, get_results_card

nav = Navbar()
footer = Footer()

with open('assets/risk_calculators/mortality/model_with_lab.pkl', 'rb') as file:
    labs = pickle.load(file)

with open('assets/risk_calculators/mortality/model_without_lab.pkl', 'rb') as file:
    no_labs = pickle.load(file)

labs_model_mort = labs["model"]
labs_imputer_mort = labs["imputer"]
labs_features_mort = labs["json"]

no_labs_model_mort = no_labs["model"]
no_labs_imputer_mort = no_labs["imputer"]
no_labs_features_mort = no_labs["json"]

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
              html.H2("Mortality Risk Calculator")
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
                         """ **Data** (as of 04/15/2020): Our model is trained on 496 patients (out of whom 201 deceased) hospitalized due to COVID-19 at the Azienda \
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
        )
    ] + \
        get_labs_indicator('lab_values_indicator') + \
        get_model_desc('mortality-model-desc') + \
        get_feature_importance('feature-importance-bar-graph') + \
        get_feature_cards('features-mortality') + \
        get_submit_button('submit-features-calc') + \
        get_results_card('score-calculator-card-body','calc-input-error') + \
        get_inputed_vals('imputed-text-mortality'),
        className="page-body"
    )


def RiskCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input_mort(labs,feature_vals):
    if labs:
        features = labs_features_mort
        imputer = labs_imputer_mort
    else:
        features = no_labs_features_mort
        imputer = no_labs_imputer_mort
    length = len(features["numeric"])
    return valid_input(features["numeric"],feature_vals[0],length)

def predict_risk_mort(labs,feature_vals):
    if labs:
        model = labs_model_mort
        features = labs_features_mort
        imputer = labs_imputer_mort
    else:
        model = no_labs_model_mort
        features = no_labs_features_mort
        imputer = no_labs_imputer_mort
    score = predict_risk(model,features,imputer,feature_vals)
    card_content = [
        html.H4("The mortality risk score is:",className="score-calculator-card-content"),
        html.H4(score,className="score-calculator-card-content"),
    ]
    impute_text = 'None'
    return card_content,impute_text
