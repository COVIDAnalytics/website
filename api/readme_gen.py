import pickle

paths = [
    "../assets/risk_calculators/infection/model_without_lab.pkl",
    "../assets/risk_calculators/infection/model_with_lab.pkl",
    "../assets/risk_calculators/mortality/model_without_lab.pkl",
    "../assets/risk_calculators/mortality/model_with_lab.pkl"
]

inv_map = {
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
mapping = {v: k for k, v in inv_map.items()}

numeric = {}
comorb = {}
cat = {}
for path in paths: 
    json = pickle.load(open(path, "rb"))["json"]
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
                exp = feature["explanation"]
                if feature["name"] == "Gender":
                    exp += ". 0.0 -> male; 1.0 -> female"
                cat[feature["name"]] = "category | " + str(feature["vals"]) + "\t| " + exp
print("| Get Param\t| Feature Name" + ('\t' * 4) + "| Datatype | Value Range\t| Explanation |")
print("|-----------\t| ------------" + ('\t' * 4) + "| -------- | -----------\t| ----------- |")
namecol = 5
for key, val in numeric.items(): 
    tabs = namecol - int(round(len(key) / 8))
    tabs2 = 2 - int(len(mapping[key]) / 8)
    print("|`{}`{}|  {}{}| {} |".format(mapping[key], '\t' * tabs2, key, "\t" * tabs, str(val)))
print("Categorical")
for key, val in cat.items(): 
    print("|`{}`\t\t| {}\t\t\t\t\t\t| {} |".format(mapping[key], key, str(val)))
print("Comorbitiites")
for key, val in comorb.items(): 
    tabs = namecol - int(round(len(key) / 8))
    tabs2 = 2 - int(len(mapping[key]) / 8)
    print("|`{}`{}| {}{}| {} |".format(mapping[key], '\t' * tabs2, key, '\t' * tabs, str(val)))
