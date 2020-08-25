import base64
from io import BytesIO
import pickle

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc

from risk_calculator.infection.calculator import predict_risk_infec, get_languages
from treatment_calculator.features import build_feature_cards
import numpy as np

from treatment_calculator.utils import build_results_graph


def register_callbacks(app):
    with open('assets/treatment_calculators/COMORB_DEATH/CORTICOSTEROIDS.pkl', 'rb') as pkl:
        cd_corti = pickle.load(pkl)

    model_names = ['lr', 'rf', 'cart', 'qda', 'gb'] # add xgboost
    treatment_models = cd_corti["treatment-models"]
    no_treatment_models = cd_corti["no-treatment-models"]
    treatment_features = cd_corti["json"]
    print(cd_corti)

    @app.callback(
        Output('treatments-calc-feature-cards', 'children'),
        [Input("treatments-calc-tabs", "value"),
         Input('treatments-calc-language', 'value')])
    def get_infection_model_feat_cards(tabs, language):
        return build_feature_cards(treatment_features, False, False, language)

    @app.callback(
        [Output('treatments-calc-tabs', 'value'),
         Output('treatments-results-graph', 'children')],
        [Input('treatments-calc-language', 'value'),
         Input('submit-treatments-calc', 'n_clicks'),
         Input('treatments-sel', 'value')],
        [State({'type': 'treatments-checkbox', 'feature': ALL, 'index': ALL, 'f_idx': ALL}, 'checked'),
         State({'type': 'treatments', 'feature': ALL, 'index': ALL, 'f_idx': ALL, 'f_def': ALL}, 'value'),
         State({'type': 'treatments-multi', 'feature': ALL, 'index': ALL,}, 'value')]
    )
    def calc_risk_score_mortality(*argv):
        language = argv[0]
        submit = argv[1]
        treatment = argv[2]

        print("SUBMIT: " + str(submit))
        if submit is None:
            return ["tabs-1", []]
        checkbox_features = dash.callback_context.states_list[0]
        other_features = dash.callback_context.states_list[1]
        multi_features = dash.callback_context.states_list[2]
        print("GOAT")
        print(argv)
        print(checkbox_features)
        print(other_features)
        print(multi_features)

        X = [0] * 100

        for feat in checkbox_features:
            if feat["value"] is True:
                X[feat["id"]["f_idx"]] = 1

        no_inputs = 0
        for feat in other_features:
            if "value" in feat:
                # user gave input
                X[feat["id"]["f_idx"]] = feat["value"]
            else:
                # user gave no input
                X[feat["id"]["f_idx"]] = feat["id"]["f_def"]
                no_inputs += 1

        for feat in multi_features:
            for idx in feat["value"]:
                X[idx] = 1

        num_features = 0
        for name in model_names:
            model = treatment_models[name]["model"]
            try:
                #print("FEATURES" + str(model.coef_.shape[-1]))
                num_features = model.n_features_
            except:
                pass

        X = X[0:num_features]
        X = np.array(X).reshape(1, -1)
        print("X = ")
        print(X)

        results = {"treat": {}, "ntreat": {}, "avgtreat": 0.0, "avgntreat": 0.0}
        for name in model_names:
            tmodel = treatment_models[name]["model"]
            ntmodel = no_treatment_models[name]["model"]
            results["treat"][name] = tmodel.predict_proba(X)[0][0]
            results["ntreat"][name] = ntmodel.predict_proba(X)[0][0]
            results["avgtreat"] += results["treat"][name]
            results["avgntreat"] += results["ntreat"][name]

            print("predict_proba(X) for " + name)
            print(str(ntmodel.predict_proba(X)) + ", " + str(tmodel.predict_proba(X)))

        results["avgtreat"] /= len(model_names)
        results["avgntreat"] /= len(model_names)

        graph = build_results_graph(results, model_names, treatment)

        return ["tab-2", [graph]]
