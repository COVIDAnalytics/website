import math

import dash_html_components as html
import dash_bootstrap_components as dbc
import visdcc

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import predict_risk, langs
from risk_calculator.visuals import get_labs_indicator, get_model_desc, get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_submit_button, get_results_card
from risk_calculator.visuals import get_lang, get_page_desc, get_personal_visual

def InfectionRiskCalc():
    nav = Navbar()
    footer = Footer()

    body = dbc.Container(
        get_lang('language-calc-infection') +
        get_page_desc('page-desc-infection') +
        get_labs_indicator('lab_values_indicator_infection') +
        get_feature_cards('features-infection') +
        get_submit_button('submit-features-calc-infection') +
        get_results_card('score-calculator-card-body-infection', 'calc-input-error-infection') +
        get_inputed_vals('imputed-text-infection') +
        get_personal_visual('visual-1-infection') +
        get_model_desc('infection-model-desc') +
        get_feature_importance('feature-importance-bar-graph-infection'),
        className="page-body"
    )
    layout = html.Div([
        nav, body, footer], className="site")
    return layout


# Builds language dictionaries from language modules
def get_languages(labs_auc, labs_population, labs_positive, no_labs_auc, no_labs_population, no_labs_positive):
    return {
        "page_desc_infection": {
            num: lan.get_page_desc_infection() for (num, lan) in zip(range(len(langs)), langs)
        },
        "insert_feat_text": {
            num: lan.get_insert_feat() for (num, lan) in zip(range(len(langs)), langs)
        },
        "oxygen": {
            num: lan.get_oxygen_text() for (num, lan) in zip(range(len(langs)), langs)
        },
        "submit": {
            num: lan.submit for (num, lan) in zip(range(len(langs)), langs)
        },
        "results_card_infection": {
            num: lan.get_results_card_infection() for (num, lan) in zip(range(len(langs)), langs)
        },
        "technical_details_infection_labs": {
            num: lan.get_model_desc_infection(labs_auc, labs_population, labs_positive)
                for (num, lan) in zip(range(len(langs)), langs)
        },
        "technical_details_infection_no_labs": {
            num: lan.get_model_desc_infection(no_labs_auc, no_labs_population, no_labs_positive)
             for (num, lan) in zip(range(len(langs)), langs)
        },
        "visual_1": {
            num: lan.get_visual_1() for (num, lan) in zip(range(len(langs)), langs)
        }
    }


def predict_risk_infec(cols, model, features, imputer, explainer, feature_vals, temp_unit, card_text, language):
    score, impute_text, plot = predict_risk(False, model, features, imputer, explainer,
                                            feature_vals, cols, temp_unit, language)
    """Given features, other input, etc. calculate a score and return score_card, imputed_text, and user plot"""
    card_content = [
        html.H4(card_text[0], className="score-calculator-card-content-infection"),
        html.H4(str(int(math.floor(score/10.0)))+card_text[1], className="score-calculator-card-content-infection"),
    ]
    return card_content, impute_text, plot
