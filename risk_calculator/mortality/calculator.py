import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import predict_risk
from risk_calculator.visuals import get_labs_indicator, get_model_desc, get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_submit_button, get_results_card
from risk_calculator.visuals import get_lang, get_page_desc, get_personal_visual

import risk_calculator.languages.english as english
import risk_calculator.languages.spanish as spanish
import risk_calculator.languages.italian as italian
import risk_calculator.languages.german as german


def RiskCalc():
    nav = Navbar()
    footer = Footer()
    body = dbc.Container(
            get_lang('language-calc-mortality') +
            get_page_desc('page-desc-mortality') +
            get_labs_indicator('lab_values_indicator') +
            get_feature_cards('features-mortality') +
            get_submit_button('submit-features-calc') +
            get_results_card('score-calculator-card-body', 'calc-input-error') +
            get_inputed_vals('imputed-text-mortality') +
            get_personal_visual('visual-1-mortality') +
            get_model_desc('mortality-model-desc') +
            get_feature_importance('feature-importance-bar-graph'),
            className="page-body"
        )

    layout = html.Div([nav, body, footer], className="site")
    return layout


def get_languages(labs_auc, labs_population, labs_positive, no_labs_auc, no_labs_population, no_labs_positive):
    langs = [english, spanish, italian, german]  # corresponds to [0, 1, 2, 3]
    return {
        "page_desc_mortality": {
            num: lan.get_page_desc_mortality(labs_auc, no_labs_auc) for (num, lan) in zip(range(len(langs)), langs)
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
        "results_card_mortality": {
            num: lan.get_results_card_mortality() for (num, lan) in zip(range(len(langs)), langs)
        },
        "technical_details_mortality_labs": {
            num: lan.get_model_desc_mortality(labs_auc, labs_population, labs_positive)
            for (num, lan) in zip(range(len(langs)), langs)
        },
        "technical_details_mortality_no_labs": {
            num: lan.get_model_desc_mortality(no_labs_auc, no_labs_population, no_labs_positive)
            for (num, lan) in zip(range(len(langs)), langs)
        },
        "visual_1": {
            num: lan.get_visual_1() for (num, lan) in zip(range(len(langs)), langs)
        }
    }


def predict_risk_mort(cols, model, features, imputer, explainer, feature_vals, temp_unit, card_text, language):
    """Given features, other input, etc. calculate a score and return score_card, imputed_text, and user plot"""
    score, imputed_text, plot = predict_risk(True, model, features, imputer, explainer,
                                             feature_vals, cols, temp_unit, language)
    card_content = [
        html.H4(card_text, className="score-calculator-card-content"),
        html.H4(str(score)+"%", className="score-calculator-card-content"),
    ]
    return card_content, imputed_text, plot
