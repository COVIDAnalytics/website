import pickle
import sklearn
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

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

with open('assets/risk_calculators/infection/model_with_lab.pkl', 'rb') as file:
    labs = pickle.load(file)

with open('assets/risk_calculators/infection/model_without_lab.pkl', 'rb') as file:
    no_labs = pickle.load(file)

labs_model_infec = labs["model"]
labs_imputer_infec = labs["imputer"]
labs_features_infec = labs["json"]

no_labs_model_infec = no_labs["model"]
no_labs_imputer_infec = no_labs["imputer"]
no_labs_features_infec = no_labs["json"]

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
        )
    ] + \
    get_labs_indicator('lab_values_indicator_infection') + \
    get_model_desc('infection-model-desc') + \
    get_feature_importance('feature-importance-bar-graph-infection') + \
    get_feature_cards('features-infection') + \
    get_submit_button('submit-features-calc-infection') + \
    get_results_card('score-calculator-card-body-infection','calc-input-error-infection') + \
    get_inputed_vals('imputed-text-infection'),
    className="page-body"
)

def InfectionRiskCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input_infec(labs,feature_vals):
    if labs:
        features = labs_features_infec
        imputer = labs_imputer_infec
    else:
        features = no_labs_features_infec
        imputer = no_labs_imputer_infec
    length = len(features["numeric"])
    return valid_input(features["numeric"],feature_vals[0],length)

def predict_risk_infec(labs,feature_vals):
    if labs:
        cols = ['C-Reactive Protein (CRP)', 'Blood Calcium', 'CBC: Leukocytes', 'Aspartate Aminotransferase (AST)', \
        'ABG: PaO2', 'Age', 'Prothrombin Time (INR)', 'CBC: Hemoglobin', 'ABG: pH', 'Cholinesterase', 'Respiratory Frequency', \
        'Blood Urea Nitrogen (BUN)', 'ABG: MetHb', 'Temperature Celsius', 'Total Bilirubin', 'Systolic Blood Pressure', \
        'CBC: Mean Corpuscular Volume (MCV)', 'Glycemia', 'Cardiac Frequency', 'Sex']
    else:
        cols = ['Age', 'Cardiac Frequency', 'Respiratory Frequency', 'SaO2', 'Sex', 'Systolic Blood Pressure', 'Temperature Celsius']
    if labs:
        model = labs_model_infec
        features = labs_features_infec
        imputer = labs_imputer_infec
    else:
        model = no_labs_model_infec
        features = no_labs_features_infec
        imputer = no_labs_imputer_infec
    score = predict_risk(False,model,features,imputer,feature_vals,cols)
    card_content = [
        html.H4("The infection risk score is:",className="score-calculator-card-content-infection"),
        html.H4(score,className="score-calculator-card-content-infection"),
    ]
    impute_text = 'None'
    #impute text
    return card_content,impute_text
