import numpy as np
import pandas as pd
import math
import dash_core_components as dcc

oxygen = 'Oxygen Saturation'

title_mapping = {
    'ABG: Oxygen Saturation (SaO2)': oxygen,
    'Alanine Aminotransferase (ALT)': 'Alanine Aminotransferase (ALT)',
    'Age': 'Age',
    'Aspartate Aminotransferase (AST)': 'Aspartate Aminotransferase',
    'Blood Creatinine': 'Creatinine',
    'Blood Sodium': 'Sodium',
    'Blood Urea Nitrogen (BUN)': 'Blood Urea Nitrogen (BUN)',
    'Body Temperature': 'Temperature',
    'C-Reactive Protein (CRP)':  'C-Reactive Protein',
    'CBC: Hemoglobin': 'Hemoglobin',
    'CBC: Leukocytes': 'Leukocytes',
    'CBC: Mean Corpuscular Volume (MCV)': 'Mean Corpuscular Volume',
    'CBC: Platelets': 'Platelets',
    'Cardiac Frequency': 'Heart Rate',
    'Cardiac dysrhythmias': 'Cardiac dysrhythmias',
    'Gender' : 'Gender',
    'Glycemia': 'Glycemia',
    'Potassium Blood Level': 'Potassium',
    'Prothrombin Time (INR)': 'Prothrombin Time',
    'Systolic Blood Pressure': 'Systolic Blood Pressure (SYS)',
    'SaO2': oxygen,
    'Blood Calcium': 'Calcium',
    'ABG: PaO2': 'Partial Pressure Oxygen (PaO2)',
    'ABG: pH': 'Arterial Blood Gas pH',
    'Cholinesterase': 'Cholinesterase',
    'Respiratory Frequency': 'Respiratory Frequency',
    'ABG: MetHb': 'Arterial Blood Gas Methemoglobinemia',
    'Total Bilirubin': 'Total Bilirubin',
    'Comorbidities':'Comorbidities'
}

def convert_temp_units(x):
    return x*9/5+32

def labs_ques(val):
    return "Yes" if val else "No"

def get_oxygen_ind(feats):
    for i,f in enumerate(feats):
        if title_mapping[f["name"]] == oxygen:
            return i
    return None

def valid_input(features,feature_vals,length):
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
            if title_mapping[name] == oxygen and (val == 1 or val == 0):
                continue
            if val < min_val or val > max_val:
                return False, "Please insert a numeric value for {} between {} and {}".format(title_mapping[name],min_val,max_val),feature_vals
    threshold = math.floor(2*length/3)
    if missing > threshold:
        return False, "Please insert at least {} numeric values.".format(threshold), feature_vals
    return True,"",feature_vals

def predict_risk(m,model,features,imputer,feature_vals,columns):
    x = [0]*len(model.feature_importances_)
    #if temperature is in F, switch measurement to Celsius
    convert_temperature = feature_vals[-1] == "°C"
    #align order of feature vector so that values are in correct order
    i = 0
    for feat in features["categorical"]:
        x[feat["index"]] = feature_vals[i]
        i+=1
    for f,feat in enumerate(features["numeric"]):
        if feat["name"] == "Body Temperature" and convert_temperature:
            x[feat["index"]] = convert_temp_units(feature_vals[i])
        elif title_mapping[feat["name"]] == oxygen:
            x[feat["index"]] = 1 if feature_vals[i] > 92 else 0
        else:
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
        text = 'The missing feature, ' + title_mapping[columns[ind]] + ', was calculated as '
        if title_mapping[columns[ind]] == oxygen:
            if x_full[0][ind] == 1:
                text += '>92 (Shortness of breath)'
            else:
                text += '<92 (No shortness of breath)'
        else:
            text += str(round(x_full[0][ind],2))
        if columns[ind] == 'Body Temperature':
            impute_text[i] = text + '°F.'
        else:
            impute_text[i] = text + '.'
    impute_text = '  \n'.join(impute_text)
    return score,impute_text
