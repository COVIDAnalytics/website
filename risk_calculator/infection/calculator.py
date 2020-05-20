import math

import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import predict_risk, valid_input
from risk_calculator.visuals import get_labs_indicator,get_model_desc,get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_submit_button, get_results_card
from risk_calculator.visuals import get_lang,get_page_desc, get_personal_visual

import risk_calculator.english as english
import risk_calculator.spanish as spanish
import risk_calculator.italian as italian

def InfectionRiskCalc():
    nav = Navbar()
    footer = Footer()

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

    layout = html.Div([nav, body, footer], className="site")
    return layout

def get_languages(labs_auc,labs_population,labs_positive,no_labs_auc,no_labs_population,no_labs_positive):
    return {
        "page_desc_infection": {
            0: english.get_page_desc_infection(),
            1: spanish.get_page_desc_infection(),
            2: italian.get_page_desc_infection(),
        },
        "insert_feat_text": {
            0: english.get_insert_feat(),
            1: spanish.get_insert_feat(),
            2: italian.get_insert_feat()
        },
        "oxygen": {
            0: english.get_oxygen_text(),
            1: spanish.get_oxygen_text(),
            2: italian.get_oxygen_text()
        },
        "submit": {
            0: english.submit,
            1: spanish.submit,
            2: italian.submit
        },
        "results_card_infection": {
            0: english.get_results_card_infection(),
            1: spanish.get_results_card_infection(),
            2: italian.get_results_card_infection()
        },
        "technical_details_infection_labs": {
            0: english.get_model_desc_infection(True,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            1: spanish.get_model_desc_infection(True,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            2: italian.get_model_desc_infection(True,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive)
        },
        "technical_details_infection_no_labs": {
            0: english.get_model_desc_infection(False,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            1: spanish.get_model_desc_infection(False,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            2: italian.get_model_desc_infection(False,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive)
        },
        "visual_1": {
            0: english.get_visual_1(),
            1: spanish.get_visual_1(),
            2: italian.get_visual_1()
        }
    }


def predict_risk_infec(cols,model,features,imputer,explainer,feature_vals,temp_unit,card_text,language):
    score,impute_text,plot = predict_risk(False,model,features,imputer,explainer,feature_vals,cols,temp_unit,language)
    card_content = [
        html.H4(card_text[0],className="score-calculator-card-content-infection"),
        html.H4(str(int(math.floor(score/10.0)))+card_text[1],className="score-calculator-card-content-infection"),
    ]
    return card_content,impute_text,plot
