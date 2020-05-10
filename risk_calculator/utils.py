import numpy as np
import pandas as pd
import math
import shap
import pickle
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import risk_calculator.english as english
import risk_calculator.spanish as spanish
import risk_calculator.italian as italian

with open('assets/risk_calculators/mortality/model_with_lab.pkl', 'rb') as file:
    mort_labs = pickle.load(file)

with open('assets/risk_calculators/mortality/model_without_lab.pkl', 'rb') as file:
    mort_no_labs = pickle.load(file)

labs_model_mort = mort_labs["model"]
labs_imputer_mort = mort_labs["imputer"]
labs_features_mort = mort_labs["json"]
cols_labs_mort = mort_labs["columns"]
labs_auc_mort = mort_labs["AUC"]
labs_population_mort = [mort_labs["Size Training"],mort_labs["Size Test"]]
labs_positive_mort = [mort_labs["Percentage Training"],mort_labs["Percentage Test"]]
labs_explainer_mort = mort_labs["explainer"]
labs_importance_mort = mort_labs["importance"]

no_labs_model_mort = mort_no_labs["model"]
no_labs_imputer_mort = mort_no_labs["imputer"]
no_labs_features_mort = mort_no_labs["json"]
cols_no_labs_mort = mort_no_labs["columns"]
no_labs_auc_mort = mort_no_labs["AUC"]
no_labs_population_mort = [mort_no_labs["Size Training"],mort_no_labs["Size Test"]]
no_labs_positive_mort = [mort_no_labs["Percentage Training"],mort_no_labs["Percentage Test"]]
no_labs_explainer_mort = mort_no_labs["explainer"]
no_labs_importance_mort = mort_no_labs["importance"]

with open('assets/risk_calculators/infection/model_with_lab.pkl', 'rb') as file:
    infec_labs = pickle.load(file)

with open('assets/risk_calculators/infection/model_without_lab.pkl', 'rb') as file:
    infec_no_labs = pickle.load(file)

labs_model_infec = infec_labs["model"]
labs_imputer_infec = infec_labs["imputer"]
labs_features_infec = infec_labs["json"]
cols_labs_infec = infec_labs["columns"]
labs_auc_infec = infec_labs["AUC"]
labs_population_infec = [infec_labs["Size Training"],infec_labs["Size Test"]]
labs_positive_infec = [infec_labs["Percentage Training"],infec_labs["Percentage Test"]]
labs_explainer_infec = infec_labs["explainer"]
labs_importance_infec = infec_labs["importance"]

no_labs_model_infec = infec_no_labs["model"]
no_labs_imputer_infec = infec_no_labs["imputer"]
no_labs_features_infec = infec_no_labs["json"]
cols_no_labs_infec = infec_no_labs["columns"]
no_labs_auc_infec = infec_no_labs["AUC"]
no_labs_population_infec = [infec_no_labs["Size Training"],infec_no_labs["Size Test"]]
no_labs_positive_infec = [infec_no_labs["Percentage Training"],infec_no_labs["Percentage Test"]]
no_labs_explainer_infec = infec_no_labs["explainer"]
no_labs_importance_infec = infec_no_labs["importance"]

matplotlib.use('Agg')
oxygen = 'Oxygen Saturation'

title_mapping = {
    0: english.feature_names,
    1: spanish.feature_names,
    2: italian.feature_names
}

languages = {
    "page_desc_mortality": {
        0: english.get_page_desc_mortality(labs_auc_mort,no_labs_auc_mort),
        1: spanish.get_page_desc_mortality(labs_auc_mort,no_labs_auc_mort),
        2: italian.get_page_desc_mortality(labs_auc_mort,no_labs_auc_mort),
    },
    "page_desc_infection": {
        0: english.page_desc_infection,
        1: spanish.page_desc_infection,
        2: italian.page_desc_infection,
    },
    "insert_feat_text": {
        0: english.insert_feat,
        1: spanish.insert_feat,
        2: italian.insert_feat
    },
    "oxygen": {
        0: english.oxygen_text,
        1: spanish.oxygen_text,
        2: italian.oxygen_text
    },
    "submit": {
        0: english.submit,
        1: spanish.submit,
        2: italian.submit
    },
    "results_card_mortality": {
        0: english.results_card_mortality,
        1: spanish.results_card_mortality,
        2: italian.results_card_mortality
    },
    "results_card_infection": {
        0: english.results_card_infection,
        1: spanish.results_card_infection,
        2: italian.results_card_infection
    },
    "technical_details_mortality_labs": {
        0: english.get_model_desc_mortality(True,labs_auc_mort,no_labs_auc_mort,labs_population_mort,no_labs_population_mort,labs_positive_mort,no_labs_positive_mort),
        1: spanish.get_model_desc_mortality(True,labs_auc_mort,no_labs_auc_mort,labs_population_mort,no_labs_population_mort,labs_positive_mort,no_labs_positive_mort),
        2: italian.get_model_desc_mortality(True,labs_auc_mort,no_labs_auc_mort,labs_population_mort,no_labs_population_mort,labs_positive_mort,no_labs_positive_mort)
    },
    "technical_details_mortality_no_labs": {
        0: english.get_model_desc_mortality(False,labs_auc_mort,no_labs_auc_mort,labs_population_mort,no_labs_population_mort,labs_positive_mort,no_labs_positive_mort),
        1: spanish.get_model_desc_mortality(False,labs_auc_mort,no_labs_auc_mort,labs_population_mort,no_labs_population_mort,labs_positive_mort,no_labs_positive_mort),
        2: italian.get_model_desc_mortality(False,labs_auc_mort,no_labs_auc_mort,labs_population_mort,no_labs_population_mort,labs_positive_mort,no_labs_positive_mort)
    },
    "technical_details_infection_labs": {
        0: english.get_model_desc_infection(True,labs_auc_infec,no_labs_auc_infec,labs_population_infec,no_labs_population_infec,labs_positive_infec,no_labs_positive_infec),
        1: spanish.get_model_desc_infection(True,labs_auc_infec,no_labs_auc_infec,labs_population_infec,no_labs_population_infec,labs_positive_infec,no_labs_positive_infec),
        2: italian.get_model_desc_infection(True,labs_auc_infec,no_labs_auc_infec,labs_population_infec,no_labs_population_infec,labs_positive_infec,no_labs_positive_infec)
    },
    "technical_details_infection_no_labs": {
        0: english.get_model_desc_infection(False,labs_auc_infec,no_labs_auc_infec,labs_population_infec,no_labs_population_infec,labs_positive_infec,no_labs_positive_infec),
        1: spanish.get_model_desc_infection(False,labs_auc_infec,no_labs_auc_infec,labs_population_infec,no_labs_population_infec,labs_positive_infec,no_labs_positive_infec),
        2: italian.get_model_desc_infection(False,labs_auc_infec,no_labs_auc_infec,labs_population_infec,no_labs_population_infec,labs_positive_infec,no_labs_positive_infec)
    },
    "visual_1": {
        0: english.visual_1,
        1: spanish.visual_1,
        2: italian.visual_1
    }
}

def convert_temp_units(x):
    return x*9/5+32

def labs_ques(val,language):
    if language == 0:
        return "Yes" if val else "No"
    if language == 1:
        return "Si" if val else "No"
    return "Sì" if val else "No"

def oxygen_vals(val,language):
    if language == 0:
        return "Yes" if val == 92 else "No"
    if language == 1:
        return "Si" if val == 92 else "No"
    return "Sì" if val == 92 else "No"

def get_oxygen_ind(feats):
    for i,f in enumerate(feats):
        if title_mapping[0][f["name"]] == oxygen:
            return i
    return None

def valid_input(features,feature_vals,length,language):
    #assume theres only one categorical
    numerics = feature_vals[1:length+1]
    missing = 0
    for feat in range(length):
        val = numerics[feat]
        if val is None:
            if features[feat]["name"] == "Age":
                return False, "Please insert a value for Age.", feature_vals
            feature_vals[feat+1] = np.nan
            missing += 1
        else:
            content = features[feat]
            name = content["name"]
            min_val = content["min_val"]
            max_val = content["max_val"]
            if title_mapping[0][name] == oxygen and (val == 1 or val == 0):
                continue
            if val < min_val or val > max_val:
                text = [
                "Please insert a numeric value for {} between {} and {}".format(title_mapping[language][name],min_val,max_val),
                "Por favor inserte un valor numérico para {} entre {} y {}".format(title_mapping[language][name],min_val,max_val),
                "Inserisci un valore numerico per {} fra {} e {}".format(title_mapping[language][name],min_val,max_val)
                ]
                return False,text[language],feature_vals
    threshold = math.floor(2*length/3)
    if missing > threshold:
        text = [
        "Please insert at least {} numeric values.".format(threshold),
        "Por favor inserte al menos {} valores numericos.".format(title_mapping[language][name]),
        "Si prega di inserire almeno {} valori numerici.".format(title_mapping[language][name])
        ]
        return False,text[language],feature_vals
    return True,"",feature_vals

def predict_risk(m,model,features,imputer,explainer,feature_vals,columns,temp_unit,labs,language):
    x = [0]*len(model.feature_importances_)
    #if temperature is in F, switch measurement to Celsius
    convert_temperature = temp_unit[0] == "°C"
    #align order of feature vector so that values are in correct order
    i = 0
    for feat in features["categorical"]:
        x[feat["index"]] = feature_vals[i]
        i+=1
    for f,feat in enumerate(features["numeric"]):
        if feat["name"] == "Body Temperature" and convert_temperature:
            x[feat["index"]] = convert_temp_units(feature_vals[i])
        else:
            x[feat["index"]] = feature_vals[i]
        i+=1
    if m:
        comorbidities = feature_vals[i]
        indexes = features["multidrop"][0]["index"]
        for c in comorbidities:
            ind = features["multidrop"][0]["vals"].index(c)
            x[indexes[ind]] = 1
    imputed = np.argwhere(np.isnan(x))
    x_full = imputer.transform([x])
    X = pd.DataFrame(columns = columns, index = range(1), dtype=np.float)
    X.loc[0]=x_full[0]
    score = model.predict_proba(X)[:,1]
    score = int(100*round(score[0], 2))
    impute_text = [''] * len(imputed)
    missing_text = [
        ['The missing feature, ',', was calculated as '],
        ['La característica que falta, ', ' fue calculado como '],
        ['La caratteristica mancante, ', ' è stato calcolato come '],
        ]
    for i,ind in enumerate(imputed):
        ind = int(ind)
        text = missing_text[language][0] + title_mapping[language][columns[ind]] + missing_text[language][1]
        text += str(round(x_full[0][ind],2))
        if columns[ind] == 'Body Temperature':
            impute_text[i] = text + '°F.'
        else:
            impute_text[i] = text + '.'
    impute_text = '  \n'.join(impute_text)
    shap_new = explainer.shap_values(X)
    names = ['\n'.join(wrap(''.join(['{}'.format(title_mapping[language][c])]), width=12)) for c in columns]
    plot = shap.force_plot(
        np.around(explainer.expected_value, decimals=2),
        np.around(shap_new, decimals=2),
        np.around(X, decimals=2) ,
        link = "logit",
        matplotlib = True,
        show = False,
        feature_names=names
    )
    plt.axis('off') # this rows the rectangular frame
    return score,impute_text,plot

def build_lab_ques_card(lang):
    q = ["Do you have lab values?","¿Tienes valores de laboratorio?","Hai valori di laboratorio?"]
    return q[lang]
