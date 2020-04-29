import numpy as np
import pandas as pd
import math
import dash_core_components as dcc

def convert_temp_units(x):
    return (x-32)/1.8

def fix_title(name):
    if name == "Temperature Celsius":
        return "Body Temperature"
    if name == "Sex":
        return "Gender"
    return name

def valid_input(features,feature_vals,length):
    numerics = feature_vals[:length]
    missing = 0
    for feat in range(length):
        val = numerics[feat]
        if val is None:
            if features[feat]["name"] == "Age":
                return False, "Please insert a value for Age.", feature_vals
            feature_vals[feat] = np.nan
            missing += 1
        else:
            content = features[feat]
            name = content["name"]
            min_val = content["min_val"]
            max_val = content["max_val"]
            if val < min_val or val > max_val:
                return False, "Please insert a numeric value for {} between {} and {}".format(name,min_val,max_val),feature_vals
    threshold = math.floor(2*length/3)
    if missing > threshold:
        return False, "Please insert at least {} numeric values.".format(threshold), feature_vals
    return True,"",feature_vals

def predict_risk(m,model,features,imputer,feature_vals,columns):
    x = [0]*len(model.feature_importances_)
    #if temperature is in F, switch measurement to Celsius
    convert_temperature = feature_vals[-1] == "°F"
    #align order of feature vector so that values are in correct order
    i = 0
    for f,feat in enumerate(features["numeric"]):
        if feat["name"] == "Body Temperature" and convert_temperature:
            x[feat["index"]] = convert_temp_units(feature_vals[i])
        else:
            x[feat["index"]] = feature_vals[i]
        i+=1
    for feat in features["categorical"]:
        x[feat["index"]] = feature_vals[i]
        i+=1
    if m:
        comorbidities = feature_vals[i]
        for c in comorbidities:
            ind = features["multidrop"][0]["vals"].index(c)
            x[ind] = 1
    imputed = np.argwhere(np.isnan(x))
    x_full = imputer.transform([x])
    X = pd.DataFrame(columns = columns, index = range(1), dtype=np.float)
    X.loc[0]=x_full[0]
    score = model.predict_proba(X)[:,1]
    score = str(int(100*round(score[0], 2)))+"%"
    impute_text = [''] * len(imputed)
    for i,ind in enumerate(imputed):
        ind = int(ind)
        if columns[ind] == 'Temperature Celsius':
            impute_text[i] = 'The missing feature, ' + fix_title(columns[ind]) + ', was calculated as ' + str(round(x_full[0][ind],2)) + '°C.'
        else:
            impute_text[i] = 'The missing feature, ' + fix_title(columns[ind]) + ', was calculated as ' + str(round(x_full[0][ind],2)) + '.'
    impute_text = '  \n'.join(impute_text)
    return score,impute_text
