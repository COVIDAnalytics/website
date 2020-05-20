import pickle

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

def RiskCalc():
    nav = Navbar()
    footer = Footer()
    body = dbc.Container(
            get_lang('language-calc-mortality') + \
            get_page_desc('page-desc-mortality') + \
            get_labs_indicator('lab_values_indicator') + \
            get_feature_cards('features-mortality') + \
            get_submit_button('submit-features-calc') + \
            get_results_card('score-calculator-card-body','calc-input-error') + \
            get_inputed_vals('imputed-text-mortality') + \
            get_personal_visual('visual-1-mortality') + \
            get_model_desc('mortality-model-desc') + \
            get_feature_importance('feature-importance-bar-graph'),
            className="page-body"
        )

    layout = html.Div([nav, body, footer], className="site")
    return layout

def get_languages(labs_auc,labs_population,labs_positive,no_labs_auc,no_labs_population,no_labs_positive):
    return {
        "page_desc_mortality": {
            0: english.get_page_desc_mortality(labs_auc,no_labs_auc),
            1: spanish.get_page_desc_mortality(labs_auc,no_labs_auc),
            2: italian.get_page_desc_mortality(labs_auc,no_labs_auc),
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
        "results_card_mortality": {
            0: english.get_results_card_mortality(),
            1: spanish.get_results_card_mortality(),
            2: italian.get_results_card_mortality()
        },
        "technical_details_mortality_labs": {
            0: english.get_model_desc_mortality(True,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            1: spanish.get_model_desc_mortality(True,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            2: italian.get_model_desc_mortality(True,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive)
        },
        "technical_details_mortality_no_labs": {
            0: english.get_model_desc_mortality(False,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            1: spanish.get_model_desc_mortality(False,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive),
            2: italian.get_model_desc_mortality(False,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive)
        },
        "visual_1": {
            0: english.get_visual_1(),
            1: spanish.get_visual_1(),
            2: italian.get_visual_1()
        }
    }



def predict_risk_mort(cols,model,features,imputer,explainer,feature_vals,temp_unit,card_text,language):
    score,imputed_text,plot = predict_risk(True,model,features,imputer,explainer,feature_vals,cols,temp_unit,language)
    card_content = [
        html.H4(card_text,className="score-calculator-card-content"),
        html.H4(str(score)+"%",className="score-calculator-card-content"),
    ]
    return card_content,imputed_text,plot
