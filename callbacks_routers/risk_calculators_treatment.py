import base64
from io import BytesIO
import pickle

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc

from risk_calculator.infection.calculator import predict_risk_infec, get_languages
from treatment_calculator.features import build_feature_cards


def register_callbacks(app):
    with open('assets/treatment_calculators/COMORB_DEATH/CORTICOSTEROIDS.pkl', 'rb') as pkl:
        cd_corti = pickle.load(pkl)

    model_names = ['lr', 'rf', 'cart', 'xgboost', 'qda', 'gb']
    treatment_models = cd_corti["treatment-models"]
    no_treatment_models = cd_corti["no-treatment-models"]
    treatment_features = cd_corti["json"]

    @app.callback(
        Output('treatments-calc-feature-cards', 'children'),
        [Input("treatments-calc-tabs", "value"),
         Input('treatments-calc-language', 'value')])
    def get_infection_model_feat_cards(tabs, language):
        return build_feature_cards(treatment_features, False, False, language)


