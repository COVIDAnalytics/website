import pickle

paths = [
    "../assets/risk_calculators/infection/model_without_lab.pkl",
    "../assets/risk_calculators/infection/model_with_lab.pkl",
    "../assets/risk_calculators/mortality/model_without_lab.pkl",
    "../assets/risk_calculators/mortality/model_with_lab.pkl"
]

numeric = {}
comorb = {}
cat = {}
for path in paths: 
    json = pickle.load(open(path, "rb"))["json"]
    print(json)
    for category, features in json.items(): 
        if category == "numeric": 
            for feature in features:  
                rang = str(feature["min_val"]) + " - " + str(feature["max_val"])
                tabs = 2 - int(len(rang) / 8)
                numeric[feature["name"]] = "numeric  | {} {}| {}".format(rang, '\t' * tabs, feature["explanation"])
        elif category == "multidrop": 
            for feature in features:  
                for com in feature["vals"]:
                    comorb[com] = "boolean  | true/false \t| Disease"
        elif category == "categorical":
            for feature in features:  
                cat[feature["name"]] = "vals: " + str(feature["vals"])

print("Feature Name" + ('\t' * 4) + " | Datatype | Value Range\t| Explanation |")
print("Numeric")
print("------------" + ('\t' * 4) + " | -------- | -----------\t| ----------- |")
for key, val in numeric.items(): 
    tabs = 5 - int(len(key) / 8)
    print("{}{} | {}".format(key, "\t" * tabs, str(val)))
print("Categorical")
for key, val in cat.items(): 
    print("{} \t\t\t| {}".format(key, str(val)))
print("Comorbitiites")
for key, val in comorb.items(): 
    tabs = 5 - int(len(key) / 8)
    print("{}{} | {}".format(key, '\t' * tabs, str(val)))
