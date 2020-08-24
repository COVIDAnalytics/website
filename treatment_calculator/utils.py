import numpy as np
import pandas as pd
import math
import shap
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap

from treatment_calculator.languages.english import English

langs = [English()]
lang_names = {
    0: "English",
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
def valid_input(numeric_features, user_features, language):
    title_mapping = get_title_mapping()
    missing = 0

    for i, user_feature in enumerate(user_features):
        f_name = user_feature["id"]["feature"]

        # Only check for numeric values
        if "numeric" in user_feature["id"]["index"]:
            user_val = user_feature["value"] if "value" in user_feature else None
            if user_val is None:
                if f_name == "Age":
                    return False, langs[language].prompt_missing_feature(f_name)
                # Change None to np.nan. +1 offset bec assume 1 catageorical at index 0
                user_features[i]["value"] = np.nan
                missing += 1
            else:
                # Find the json feature from numeric_features with the name of the current user feature
                numeric_feature = [f for f in numeric_features if f["name"] == f_name][0]

                # Lazy save the index for later (so we don't have to search the json again)
                user_features[i]["x-index"] = numeric_feature["index"]

                # Check if user provided input is within range
                min_val = numeric_feature["min_val"]
                max_val = numeric_feature["max_val"]
                if title_mapping[0][f_name] == oxygen and (user_val == 1 or user_val == 0):
                    continue
                if user_val < min_val or user_val > max_val:
                    return False, \
                        langs[language].outOfRangeValues.format(title_mapping[language][f_name], min_val, max_val),
    # user should give at least 2/3 of features
    threshold = math.floor(2 * len(numeric_features) / 3)
    if missing > threshold:
        return False, langs[language].notEnoughValues.format(threshold)
    return True, ""


# Uses model and features to predict score
def predict_risk(m, model, features, imputer, explainer, user_features, columns, language):
    x = [0] * len(model.feature_importances_)
    all_features = features["numeric"] + features["categorical"] + features["multidrop"]

    # Loop through all user provided features
    for feat in user_features:

        # Get name of current feature
        f_name = feat["id"]["feature"]

        # The index that this feature should be assigned to in the input vector, x
        index = -1

        # Check if cached index is there
        if "x-index" in feat:
            index = feat["x-index"]
        else:
            # If not, find the index
            json_feature = [f for f in all_features if f["name"] == f_name][0]
            if f_name != "Comorbidities":
                index = json_feature["index"]
            else:
                # Handle special case
                for comorb in feat["value"]:
                    c_idx = features["multidrop"][0]["vals"].index(comorb)
                    index = features["multidrop"][0]["index"][c_idx]
                    x[index] = 1
                continue

        # Assign value to right index in input vector
        x[index] = feat["value"]

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
