import dash_core_components as dcc

def convert_temp_units(x):
    return (x-32)/1.8

def valid_input(features,imputer,feature_vals):
    numeric = len(features["numeric"])
    indexes = [0] * len(feature_vals)
    for feat in range(numeric):
        val = feature_vals[feat]
        if val is None:
            feature_vals[feat] = np.nan
            indexes[feat] = 1
        else:
            content = features["numeric"][feat]
            name = content["name"]
            min_val = content["min_val"]
            max_val = content["max_val"]
            if val < min_val or val > max_val:
                return False, "Please insert a numeric value for {} between {} and {}".format(name,min_val,max_val)
    res = imputer.transform(feature_vals)
    return True,"",res,np.multiply(indexes,res)

def predict_risk(model,features,feature_vals,missing):
    x = [0]*len(model.feature_importances_)
    #if temperature is in F, switch measurement to Celsius
    convert_temperature = feature_vals[-1] == "°F"
    #align order of feature vector so that values are in correct order
    i = 0
    for feat in features["numeric"]:
        if feat["name"] == "Body Temperature" and convert_temperature:
            x[feat["index"]] = convert_temp_units(feature_vals[i])
        else:
            x[feat["index"]] = feature_vals[i]
        i+=1
    for feat in features["categorical"]:
        x[feat["index"]] = feature_vals[i]
        i+=1
    symptoms = feature_vals[i]
    comorbidities = feature_vals[i+1]
    for s in symptoms:
        ind = features["checkboxes"][0]["vals"].index(s)
        x[ind] = 1
    for c in comorbidities:
        ind = features["multidrop"][0]["vals"].index(c)
        x[ind] = 1
    score = model.predict_proba([x])[:,1]
    score = str(int(100*round(1 - score[0], 2)))+"%"
    return dash_core_components
