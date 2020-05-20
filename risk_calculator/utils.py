import numpy as np
import pandas as pd
import math
import shap
import pickle
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap

import risk_calculator.english as english
import risk_calculator.spanish as spanish
import risk_calculator.italian as italian

matplotlib.use('Agg')
oxygen = 'Oxygen Saturation'

def get_title_mapping():
    return {
        0: english.get_feature_names(),
        1: spanish.get_feature_names(),
        2: italian.get_feature_names()
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

def get_oxygen_info(cols,feats):
    oxygen_in = "SaO2" in cols or 'ABG: Oxygen Saturation (SaO2)' in cols
    title_mapping = get_title_mapping()
    for i,f in enumerate(feats):
        if title_mapping[0][f["name"]] == oxygen:
            return oxygen_in, i
    return oxygen_in, None

def valid_input(features,feature_vals,length,language):
    title_mapping = get_title_mapping()
    #assume theres only one categorical
    numerics = feature_vals[1:length+1]
    missing = 0
    for feat in range(length):
        val = numerics[feat]
        if val is None:
            if features[feat]["name"] == "Age":
                text = [
                "Please insert a value for Age.",
                "Por favor inserte un valor para Edad.",
                "Inserisci un valore per Età."
                ]
                return False, text[language], feature_vals
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
        "Por favor inserte al menos {} valores numericos.".format(threshold),
        "Si prega di inserire almeno {} valori numerici.".format(threshold)
        ]
        return False,text[language],feature_vals
    return True,"",feature_vals

def predict_risk(m,model,features,imputer,explainer,feature_vals,columns,temp_unit,language):
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
    title_mapping = get_title_mapping()
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

def switch_oxygen(vec,ind):
    #assume there is only 1 categorical variable
    ind = ind + 1
    vec = list(vec)
    vals = vec[0]
    length = len(vals)
    if length > 0 and length > ind:
        oxygen = vals[-1]
        n = len(vals)-1
        for i in range(n,ind,-1):
            vals[i] = vals[i-1]
        vals[ind] = oxygen
        vec[0] = vals
        return tuple(vec)
    vec[0] = vals
    return tuple(vec)
