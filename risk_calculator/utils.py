import numpy as np
import pandas as pd
import math
import shap
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap

import risk_calculator.languages.english as english
import risk_calculator.languages.spanish as spanish
import risk_calculator.languages.italian as italian
import risk_calculator.languages.german as german

langs = [english, spanish, italian, german]
lang_names = {
    0: "English",
    1: "Español",
    2: "Italiano",
    3: "Deutsch"
}
matplotlib.use('Agg')
oxygen = 'Oxygen Saturation'


def get_title_mapping():
    """Returns a dic that indexes language number with feature name translation. E.g. { 0: {'Age': 'Age'}, ... }"""
    return {num: lan.get_feature_names() for (num, lan) in zip(range(len(langs)), langs)}


def cvt_temp_c2f(x):
    return x*9/5+32


def labs_ques(exp, language):
    """Returns yes if exp evaluates to True"""
    return langs[language].get_yes(exp)


def oxygen_vals(val, language):
    """Returns yes if val == 92, else no"""
    return langs[language].get_yes(val == 92)


def get_oxygen_info(cols, feats):
    oxygen_in = "SaO2" in cols or 'ABG: Oxygen Saturation (SaO2)' in cols
    title_mapping = get_title_mapping()
    for i, f in enumerate(feats):
        if title_mapping[0][f["name"]] == oxygen:
            return oxygen_in, i
    return oxygen_in, None


# Validates the user input into calculator
def valid_input(features, feature_vals, length, language):
    title_mapping = get_title_mapping()
    # assume theres only one categorical
    numerics = feature_vals[1:length+1]
    missing = 0
    for feat in range(length):
        val = numerics[feat]
        if val is None:
            # TODO: This could be generalized to any feature. Should it? No, right.
            if features[feat]["name"] == "Age":
                return False, langs[language].prompt_missing_feature(features[feat]["name"]), feature_vals
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
                return False, \
                    langs[language].outOfRangeValues.format(title_mapping[language][name], min_val, max_val),\
                    feature_vals
    threshold = math.floor(2*length/3)
    if missing > threshold:
        return False, langs[language].notEnoughValues.format(threshold), feature_vals
    return True, "", feature_vals


# Uses model and features to predict score
def predict_risk(m, model, features, imputer, explainer, feature_vals, columns, temp_unit, language):
    x = [0]*len(model.feature_importances_)

    # if temperature is in F, switch measurement to Celsius
    convert_temperature = temp_unit[0] == "°C"

    # align order of feature vector so that values are in correct order
    i = 0
    for feat in features["categorical"]:
        x[feat["index"]] = feature_vals[i]
        i += 1
    for f, feat in enumerate(features["numeric"]):
        if feat["name"] == "Body Temperature" and convert_temperature:
            x[feat["index"]] = cvt_temp_c2f(feature_vals[i])
        else:
            x[feat["index"]] = feature_vals[i]
        i += 1
    if m:
        comorbidities = feature_vals[i]
        indexes = features["multidrop"][0]["index"]
        for c in comorbidities:
            ind = features["multidrop"][0]["vals"].index(c)
            x[indexes[ind]] = 1
    imputed = np.argwhere(np.isnan(x))
    x_full = imputer.transform([x])
    _X = pd.DataFrame(columns=columns, index=range(1), dtype=np.float)
    _X.loc[0] = x_full[0]
    score = model.predict_proba(_X)[:, 1]
    score = int(100*round(score[0], 2))
    impute_text = [''] * len(imputed)
    title_mapping = get_title_mapping()
    for i, ind in enumerate(imputed):
        ind = int(ind)
        temp = '°F' if columns[ind] == 'Body Temperature' else ''
        impute_text[i] = langs[language].missingFeatureTxt.format(
                title_mapping[language][columns[ind]],
                str(round(x_full[0][ind], 2)) + temp)

    impute_text = '  \n'.join(impute_text)
    shap_new = explainer.shap_values(_X)
    names = ['\n'.join(wrap(''.join(['{}'.format(title_mapping[language][c])]), width=12)) for c in columns]
    plot = shap.force_plot(
        np.around(explainer.expected_value, decimals=2),
        np.around(shap_new, decimals=2),
        np.around(_X, decimals=2),
        link="logit",
        matplotlib=True,
        show=False,
        feature_names=names
    )
    plt.axis('off')     # this rows the rectangular frame
    return score, impute_text, plot


def build_lab_ques_card(lang):
    return langs[lang].hasLabValues


def switch_oxygen(vec, ind):
    # assume there is only 1 categorical variable
    ind = ind + 1
    vec = list(vec)
    vals = vec[0]
    length = len(vals)
    if length > 0 and length > ind:
        oxy = vals[-1]
        n = len(vals)-1
        for i in range(n, ind, -1):
            vals[i] = vals[i-1]
        vals[ind] = oxy
        vec[0] = vals
        return tuple(vec)
    vec[0] = vals
    return tuple(vec)
