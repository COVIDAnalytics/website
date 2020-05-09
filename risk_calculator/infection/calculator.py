import pickle
import sklearn
import math
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import convert_temp_units, predict_risk, valid_input, get_oxygen_ind
from risk_calculator.utils import cols_labs_infec, cols_no_labs_infec, no_labs_features_infec, labs_features_infec
from risk_calculator.utils import labs_imputer_infec,no_labs_imputer_infec,labs_model_infec,no_labs_model_infec
from risk_calculator.utils import labs_explainer_infec,no_labs_explainer_infec
from risk_calculator.visuals import get_labs_indicator,get_model_desc,get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_feature_cards, get_submit_button, get_results_card
from risk_calculator.visuals import get_lang,get_page_desc, get_personal_visual

nav = Navbar()
footer = Footer()

oxygen_in_infec = "SaO2" in cols_no_labs_infec or 'ABG: Oxygen Saturation (SaO2)' in cols_no_labs_infec
oxygen_in_infec_labs = "SaO2" in cols_labs_infec or 'ABG: Oxygen Saturation (SaO2)' in cols_labs_infec
oxygen_infec_ind = get_oxygen_ind(no_labs_features_infec["numeric"])

body = dbc.Container(
    get_lang('language-calc-infection') + \
    get_page_desc('page-desc-infection') + \
    get_labs_indicator('lab_values_indicator_infection') + \
    get_feature_cards('features-infection') + \
    get_submit_button('submit-features-calc-infection') + \
    get_results_card('score-calculator-card-body-infection','calc-input-error-infection') + \
    get_inputed_vals('imputed-text-infection') + \
    get_personal_visual('visual-1-infection') + \
    get_model_desc('infection-model-desc') + \
    get_feature_importance('feature-importance-bar-graph-infection'),
    className="page-body"
)

def InfectionRiskCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input_infec(labs,feature_vals,language):
    if labs:
        features = labs_features_infec
        imputer = labs_imputer_infec
    else:
        features = no_labs_features_infec
        imputer = no_labs_imputer_infec
    length = len(features["numeric"])
    return valid_input(features["numeric"],feature_vals[0],length,language)

def predict_risk_infec(labs,feature_vals,temp_unit,card_text,language):
    if labs:
        cols = cols_labs_infec
        model = labs_model_infec
        features = labs_features_infec
        imputer = labs_imputer_infec
        explainer = labs_explainer_infec
    else:
        cols = cols_no_labs_infec
        model = no_labs_model_infec
        features = no_labs_features_infec
        imputer = no_labs_imputer_infec
        explainer = no_labs_explainer_infec
    score,impute_text,plot = predict_risk(False,model,features,imputer,explainer,feature_vals,cols,temp_unit,labs,language)
    card_content = [
        html.H4(card_text[0],className="score-calculator-card-content-infection"),
        html.H4(str(int(math.floor(score/10.0)))+card_text[1],className="score-calculator-card-content-infection"),
    ]
    return card_content,impute_text,plot
