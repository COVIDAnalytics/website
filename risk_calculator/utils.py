import numpy as np
import dash_core_components as dcc

def convert_temp_units(x):
    return (x-32)/1.8

def valid_input(features,feature_vals,length):
    numerics = feature_vals[:length]
    for feat in range(length):
        val = numerics[feat]
        if val is None:
            feature_vals[feat] = np.nan
        else:
            content = features[feat]
            name = content["name"]
            min_val = content["min_val"]
            max_val = content["max_val"]
            if val < min_val or val > max_val:
                return False, "Please insert a numeric value for {} between {} and {}".format(name,min_val,max_val),feature_vals
    return True,"",feature_vals

def predict_risk(m,model,features,imputer,feature_vals):
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
    x = imputer.transform([x])
    score = model.predict_proba(x)[:,1]
    score = str(int(100*round(1 - score[0], 2)))+"%"
    return dash_core_components
