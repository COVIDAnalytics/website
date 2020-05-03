import pickle

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import convert_temp_units, predict_risk, valid_input, get_oxygen_ind
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
cols_labs = labs["columns"]

no_labs_model_mort = no_labs["model"]
no_labs_imputer_mort = no_labs["imputer"]
no_labs_features_mort = no_labs["json"]
cols_no_labs = no_labs["columns"]

oxygen_in_mort = "SaO2" in cols_no_labs or 'ABG: Oxygen Saturation (SaO2)' in cols_no_labs
oxygen_in_mort_labs = "SaO2" in cols_labs or 'ABG: Oxygen Saturation (SaO2)' in cols_labs
oxygen_mort_labs_ind = get_oxygen_ind(labs_features_mort["numeric"])
oxygen_mort_ind = get_oxygen_ind(no_labs_features_mort["numeric"])

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Jumbotron(
                [
                    html.H2("Analytics can calculate the risk of mortality"),
                    dcc.Markdown(
                         """Severe COVID-19 patients require the most scarce health care resources, \
                         ventilators and intensive care beds. When the number of patients exceeds the \
                         availability of these resources, physicians have the difficult responsibility \
                         to prioritize between patients. To help them make an informed decision, \
                         we developed the mortality calculator for admitted COVID-19 patients.
                         """,
                    ),
                    html.Hr(),
                    dcc.Markdown(
                         """ **NOTE (This is a developmental version!):** A model is only as good as the data \
                         it is trained on. We will release new versions of the calculator as the amount of data \
                         we receive from our partner institutions increases. If you are a medical institution and \
                         are willing to contribute to our effort, please reach out to \
                         us [here](https://www.covidanalytics.io/contact).
                         """,
                    ),
                ],
                style={'paddingBottom':'0.5rem','paddingTop':'0.8rem'}
                )
            ]
            ),
        ],
        )
    ] + \
        get_labs_indicator('lab_values_indicator') + \
        get_feature_cards('features-mortality') + \
        get_submit_button('submit-features-calc') + \
        get_results_card('score-calculator-card-body','calc-input-error') + \
        get_inputed_vals('imputed-text-mortality') + \
        get_model_desc('mortality-model-desc') + \
        get_feature_importance('feature-importance-bar-graph'),
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

def predict_risk_mort(labs,feature_vals,temp_unit):
    if labs:
        cols = cols_labs
        model = labs_model_mort
        features = labs_features_mort
        imputer = labs_imputer_mort
    else:
        cols = cols_no_labs
        model = no_labs_model_mort
        features = no_labs_features_mort
        imputer = no_labs_imputer_mort
    score,imputed_text = predict_risk(True,model,features,imputer,feature_vals,cols,temp_unit,labs)
    card_content = [
        html.H4("The mortality risk score is:",className="score-calculator-card-content"),
        html.H4(score,className="score-calculator-card-content"),
    ]
    return card_content,imputed_text

def get_model_desc_mortality(labs):
    if labs:
        auc = html.Div(
             [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "The out of sample area under the curve (AUC) on 213 patients (out of whom 24% deceased) is ",
             html.Span(' 0.95', style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )
    else:
        auc = html.Div(
            [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "The out of sample area under the curve (AUC) on 213 patients (out of whom 24% deceased) is ",
             html.Span(' 0.93', style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )

    return [ \
        html.H2("Technical details"),
        dcc.Markdown(
             """
             Our model was trained on 1908 patients (out of whom 24% deceased) hospitalized due to COVID-19 in: \
             """,
        ),
        dcc.Markdown(
             """* The Italian city of Cremona ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona is one of the most severely hit italian provinces in Lombardy with several thousand positive cases to date.""",
        ),
        dcc.Markdown(
             """* [HM Hospitals](https://www.fundacionhm.com/), a leading Hospital Group in Spain with 15 general hospitals and 21 clinical \
             centres that cover the regions of Madrid, Galicia, and León. """,
        ),
        dcc.Markdown(
             """Given our training population, we are most confident about the relevance of our model to: (a) Western population; \
             (b) Severe to acute patients; (c) Congested hospitals. """,
        ),
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """Overall, the importance of the features is as follows:""",
        )
    ]
