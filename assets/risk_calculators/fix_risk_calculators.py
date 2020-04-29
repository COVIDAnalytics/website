import pickle



def fix_json(file_json):
    # Create new json
    data = {}

    # Numeric values
    data['numeric'] = [
         {'name': 'Age',
          'index': 1,
          'min_val': 18.0,
          'max_val': 100.0,
          'default': 65.0,
          'explanation': 'Age of the patient. Modeled only for adults.'},
         {'name': 'Cardiac Frequency',
          'index': 12,
          'min_val': 15.0,
          'max_val': 190.0,
          'default': 90.0,
          'explanation': 'Number of Beats per Minute.'},
         {'name': 'Body Temperature',
          'index': 23,
          'min_val': 0.00,
          'max_val': 120.00,
          'default': 98,
          'explanation': 'Body temperature measurement. Use the dropdown to select the unit (Fahrenheit or Celsius).'},
         {'name': 'Systolic Blood Pressure',
          'index': 22,
          'min_val': 50.0,
          'max_val': 250.0,
          'default': 125.00,
          'explanation': 'Systolic Blood Pressure in mmHg'},
         {'name': 'Oxygen Saturation (SaO2)',
          'index': 0,
          'min_val': 30.00,
          'max_val': 100.00,
          'default': 95.0,
          'explanation': 'Oxygen Saturation (SaO2) in %'},
         {'name': 'Glycemia',
          'index': 18,
          'min_val': 50.0,
          'max_val': 400.0,
          'default': 110.0,
          'explanation': 'Blood Glucose in mg/dL'},
         {'name': 'Alanine Aminotransferase (ALT)',
          'index': 2,
          'min_val': 1.8,
          'max_val': 80.0,
          'default': 22.00,
          'explanation': 'Alanine Aminotransferase (ALT) in U/L'},
         {'name': 'Aspartate Aminotransferase (AST)',
          'index': 3,
          'min_val': 5.00,
          'max_val': 300.0,
          'default': 30.0,
          'explanation': 'Aspartate Aminotransferase (AST) in U/L'},
         {'name': 'Blood Creatinine',
          'index': 4,
          'min_val': 0.10,
          'max_val': 15.00,
          'default': 0.80,
          'explanation': 'Blood Creatinine in mg/dL'},
         {'name': 'Blood Sodium',
          'index': 5,
          'min_val': 100.0,
          'max_val': 180.0,
          'default': 140.0,
          'explanation': 'Blood Sodium in mmol/L'},
         {'name': 'Blood Urea Nitrogen (BUN)',
          'index': 6,
          'min_val': 0.00,
          'max_val': 100.0,
          'default': 15.00,
          'explanation': 'Blood Urea Nitrogen (BUN) in mg/dL'},
         {'name': 'C-Reactive Protein (CRP)',
          'index': 7,
          'min_val': 0.00,
          'max_val': 600.00,
          'default': 0.5,
          'explanation': 'C-Reactive Protein (CRP) in mg/L'},
         {'name': 'Hemoglobin',
          'index': 8,
          'min_val': 2.00,
          'max_val': 25.00,
          'default': 15.00,
          'explanation': 'Hemoglobin in g/dL'},
         {'name': 'Leukocytes',
          'index': 9,
          'min_val': 0.2,
          'max_val': 100.0,
          'default': 6.0,
          'explanation': 'Leukocytes in 10^3/muL'},
         {'name': 'Mean Corpuscular Volume (MCV)',
          'index': 10,
          'min_val': 40.0,
          'max_val': 150.0,
          'default': 90.0,
          'explanation': 'Mean Corpuscular Volume (MCV) in fL'},
         {'name': 'Platelets',
          'index': 11,
          'min_val': 100.0,
          'max_val': 600.0,
          'default': 200.0,
          'explanation': 'Platelets in 10^3/muL'},
         {'name': 'Potassium Blood Level',
          'index': 19,
          'min_val': 2.0,
          'max_val': 8.0,
          'default': 4.0,
          'explanation': 'Potassium Blood Level in mmol/L'},
         {'name': 'Prothrombin Time Ratio (INR)',
          'index': 20,
          'min_val': 0.10,
          'max_val': 30.00,
          'default': 1.00,
          'explanation': 'Prothrombin Time Ratio (INR)'},
         ]

    data['categotical'] = file_json['categorical']
    data['multidrop'] = file_json['multidrop']

    return data



with open("./model_with_lab.pkl", "rb") as f:
    data = pickle.load(f)

data['json'] = fix_json(data['json'])


with open("./model_with_lab_final.pkl", "wb") as f:
    pickle.dump(data, f, protocol=4)
