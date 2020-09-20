import json
import pickle

from flask_restful import reqparse, Resource
import numpy as np

from risk_calculator.utils import predict_risk

# Def classes for different API Endpoints


class MortalityCalcNoLabsEndpoint(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        args = parseArgs(parser, mortality=True, use_labs=False)
        return api_calculator(args, mortality=True, use_labs=False)


class MortalityCalcLabsEndpoint(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        args = parseArgs(parser, mortality=True, use_labs=True)
        return api_calculator(args, mortality=True, use_labs=True)


class InfectionCalcNoLabsEndpoint(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        args = parseArgs(parser, mortality=False, use_labs=False)
        return api_calculator(args, mortality=False, use_labs=False)


class InfectionCalcLabsEndpoint(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        args = parseArgs(parser, mortality=False, use_labs=True)
        return api_calculator(args, mortality=False, use_labs=True)


def get_comorbs():
    """ret API params for comorbs"""
    return ['dysrh', 'kidney', 'atheros', 'diabetes']


def get_required_features(mortality, labs):
    """Returns the required features for each calculator type"""
    vitals = ['age', 'gender', 'temp', 'cardiac_freq', 'sao2']
    comorb = get_comorbs()
    if mortality and not labs:
        return vitals + comorb
    if mortality and labs:
        return vitals + comorb + \
            ['alt', 'ast', 'creat', 'sodium', 'bun', 'pot',
             'hemo', 'leuko', 'mcv', 'platel', 'crp', 'inr', 'glyc']
    if not mortality and not labs:
        return vitals + ['resp_freq']
    if not mortality and labs:
        return vitals + ['resp_freq', 'crp', 'leuko', 'calcium', 'platel', 'creat', 'mcv', 'inr', 'sodium',
                         'rdw', 'ast', 'bun', 'alt', 'bili', 'hemo']


def get_param_mapping():
    return {
       'age': 'Age',
       'sao2-labs': 'ABG: Oxygen Saturation (SaO2)',
       'sao2-nolabs': 'SaO2',
       'cardiac_freq': 'Cardiac Frequency',
       'alt': 'Alanine Aminotransferase (ALT)',
       'creat': 'Blood Creatinine',
       'sodium': 'Blood Sodium',
       'bun': 'Blood Urea Nitrogen (BUN)',
       'temp': 'Body Temperature',
       'crp': 'C-Reactive Protein (CRP)',
       'hemo': 'CBC: Hemoglobin',
       'leuko': 'CBC: Leukocytes',
       'mcv': 'CBC: Mean Corpuscular Volume (MCV)',
       'ast': 'Aspartate Aminotransferase (AST)',
       'platel': 'CBC: Platelets',
       'glyc': 'Glycemia',
       'pot': 'Potassium Blood Level',
       'inr': 'Prothrombin Time (INR)',
       'gender': 'Gender',
       'dysrh': 'Cardiac dysrhythmias',
       'kidney': 'Chronic kidney disease',
       'atheros': 'Coronary atherosclerosis and other heart disease',
       'diabetes': 'Diabetes',
       'bili': 'Total Bilirubin',
       'rdw': 'CBC: Red cell Distribution Width (RDW)',
       'resp_freq': 'Respiratory Frequency',
       'calcium': 'Blood Calcium'
    }


def parseArgs(parser, mortality, use_labs):
    comorbs = get_comorbs()
    for req in get_required_features(mortality, use_labs):
        if req in comorbs:
            parser.add_argument(req, type=bool)
        else:
            parser.add_argument(req, type=float)
    args = parser.parse_args()

    for k, v in args.items():
        if v is None:
            args[k] = np.nan

    return args




def api_calculator(params, mortality, use_labs):

    # select right model and right sao2 feature
    if use_labs:
        name = "model_with_lab"
        if "sao2" in params.keys():
            params["sao2-labs"] = params["sao2"]
            del params["sao2"]
    else:
        name = "model_without_lab"
        if "sao2" in params.keys():
            params["sao2-nolabs"] = params["sao2"]
            del params["sao2"]

    # Load only the model that's needed

    with open('assets/risk_calculators/{}/{}.pkl'.format("mortality" if mortality else "infection", name), 'rb') as m:
        loaded = pickle.load(m)

    model = loaded["model"]
    features = loaded["json"]
    imputer = loaded["imputer"]
    explainer = loaded["explainer"]
    cols = loaded["columns"]

    # transform params into Dash-style user_features list

    user_features = []
    param_mapping = get_param_mapping()

    comorb = get_comorbs()
    user_comorbs = []
    for arg, value in params.items():
        if arg in comorb:
            if value is True:
                user_comorbs.append(param_mapping[arg])
        else:
            user_features.append({
                'id': {'feature': param_mapping[arg]},
                'value': value
            })
    user_features.append({
        'id': {'feature': 'Comorbidities'},
        'value': user_comorbs
    })

    # Default to English
    if "language" not in params.keys():
        params["language"] = 0

    # Pass dash formatted input into the familiar predict_risk func
    score, imputed_text, plot = \
        predict_risk(mortality, model, features, imputer, explainer, user_features, cols, params["language"])

    return {
        "score": score,
        "imputed": imputed_text.split("\n"),
    }
