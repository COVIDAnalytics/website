import base64
from io import BytesIO
import pickle

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from risk_calculator.infection.calculator import predict_risk_infec, get_languages
from treatment_calculator.features import build_feature_cards
import numpy as np

from treatment_calculator.utils import build_results_graph, build_results_graph_v1
import pandas as pd


def register_callbacks(app):
    with open('assets/treatment_calculators/COMORB_DEATH/CORTICOSTEROIDS.pkl', 'rb') as pkl:
        cd_corti = pickle.load(pkl)

    model_names = ['rf', 'cart', 'qda', 'gb', 'xgboost']
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
         State({'type': 'treatments-multi', 'feature': ALL, 'index': ALL, }, 'value')]
    )
    def calc_risk_score_mortality(*argv):
        language = argv[0]
        submit = argv[1]
        treatment = argv[2]

        print("SUBMIT: " + str(submit))
        if submit is None:
            #raise PreventUpdate()
            print("Submitting tabs-1")
            return ["tab-1", []]
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
                # print("FEATURES" + str(model.coef_.shape[-1]))
                num_features = model.n_features_
            except:
                pass

        X = X[0:num_features]
        print(X)
        #X = np.array(X).reshape(1, -1)
        X = pd.DataFrame(np.array(X)).transpose()
        print(X)
        print(X.columns)
        X.columns = np.array(['AGE', 'DIABETES', 'HYPERTENSION', 'DISLIPIDEMIA', 'OBESITY',
                     'RENALINSUF', 'ANYLUNGDISEASE', 'AF', 'VIH', 'ANYHEARTDISEASE',
                     'ANYCEREBROVASCULARDISEASE', 'CONECTIVEDISEASE', 'LIVER_DISEASE',
                     'CANCER', 'MAXTEMPERATURE_ADMISSION', 'SAT02_BELOW92',
                     'BLOOD_PRESSURE_ABNORMAL_B', 'DDDIMER_B', 'PCR_B', 'TRANSAMINASES_B',
                     'LDL_B', 'CREATININE', 'SODIUM', 'LEUCOCYTES', 'LYMPHOCYTES',
                     'HEMOGLOBIN', 'PLATELETS', 'CLOROQUINE', 'ANTIVIRAL', 'ANTICOAGULANTS',
                     'INTERFERONOR', 'TOCILIZUMAB', 'ANTIBIOTICS', 'ACEI_ARBS',
                     'GENDER_MALE', 'RACE_CAUC', 'RACE_LATIN', 'RACE_ORIENTAL',
                     'RACE_OTHER'])

        print("X = ")
        print(X)

        results = {"treat": {}, "ntreat": {}, "avgtreat": 0.0, "avgntreat": 0.0}
        for name in model_names:
            tmodel = treatment_models[name]["model"]
            ntmodel = no_treatment_models[name]["model"]
            results["treat"][name] = tmodel.predict_proba(X)[0][1]
            results["ntreat"][name] = ntmodel.predict_proba(X)[0][1]
            results["avgtreat"] += results["treat"][name]
            results["avgntreat"] += results["ntreat"][name]

            print("predict_proba(X) for " + name)
            print(str(ntmodel.predict_proba(X)) + ", " + str(tmodel.predict_proba(X)))

        results["avgtreat"] /= len(model_names)
        results["avgntreat"] /= len(model_names)

        graph = build_results_graph_v1(results, model_names, treatment)

        return ["tab-2", [graph]]
