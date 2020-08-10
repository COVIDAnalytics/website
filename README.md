# Website for  COVID-19 ORC Research Effort

This website presents the results of our work.

Link to website: http://www.covidanalytics.io/

## Getting Started

After cloning/being up to date with the repo, run (preferably from a virtual environment):

```
pip install -r requirements.txt
```

## Workflow

To run the app locally, run from your command line:

```
python index.py
```

Then in your browser, insert the address shown in your terminal.

(To exit, CTRL+C)

Once you are done and have checked your changes locally, make a pull request.

## COVIDAnalytics REST API 

For easy integration, we provide a RESTful HTTP API. 

### Functionality
As of now, we only expose our models to calculate patient risk. The base path for this API is `https://covidanalytics.io/api/` and we provide the following functionality:

| Endpoint | Function |
| -------- | -------- |
| `mortality_calc_no_labs` | Runs the mortality risk calculator model **without** lab values |
| `mortality_calc_labs`    | Runs the mortality risk calculator model **with** lab values |
| `infection_calc_no_labs` | Runs the infection risk calculator model **without** lab values |
| `infection_calc_labs`    | Runs the infection risk calculator model **with** lab values |

### Parameters
| Get Param     | Feature Name                          | Datatype | Value Range        | Explanation |
|-----------    | ------------                          | -------- | -----------        | ----------- |
|`age`          |  Age                                  | numeric  | 0.0 - 100.0        | Age of the patient. Modeled only for adults. |
|`temp`         |  Body Temperature                     | numeric  | 34 - 104.0         | Body temperature measurement. Use the dropdown to select the unit (Fahrenheit or Celsius). |
|`cardiac_freq` |  Cardiac Frequency                    | numeric  | 40.0 - 171.0       | Number of Beats per Minute. |
|`resp_freq`    |  Respiratory Frequency                | numeric  | 14.0 - 40.0        | Number of Breaths per Minute |
|`sao2-nolabs`  |  SaO2                                 | numeric  | 80 - 100.0         | Oxygen Saturation (SaO2) in % |
|`sao2-labs`    |  ABG: Oxygen Saturation (SaO2)        | numeric  | 80 - 100.0         | Oxygen Saturation (SaO2) in % |
|`crp`          |  C-Reactive Protein (CRP)             | numeric  | 0.0 - 567.0        | C-Reactive Protein (CRP) in mg/L |
|`leuko`        |  CBC: Leukocytes                      | numeric  | 0.0 - 36.0         | Leukocytes in 10^3/muL |
|`calcium`      |  Blood Calcium                        | numeric  | 6.0 - 12.0         | Blood Calcium in mg/dL |
|`platel`       |  CBC: Platelets                       | numeric  | 20.0 - 756.0       | Platelets in 10^3/muL |
|`creat`        |  Blood Creatinine                     | numeric  | 0.0 - 11.0         | Blood Creatinine in mg/dL |
|`mcv`          |  CBC: Mean Corpuscular Volume (MCV)   | numeric  | 58.0 - 116.0       | Mean Corpuscular Volume (MCV) in fL |
|`inr`          |  Prothrombin Time (INR)               | numeric  | 0.0 - 17.0         | Prothrombin Time Ratio (INR) |
|`sodium`       |  Blood Sodium                         | numeric  | 115.0 - 166.0      | Blood Sodium in mmol/L |
|`rdw`          |  CBC: Red cell Distribution Width (RDW)| numeric | 10 - 27            | Red cell Distribution Width in % |
|`ast`          |  Aspartate Aminotransferase (AST)     | numeric  | 9.0 - 941.0        | Aspartate Aminotransferase (AST) in U/L |
|`bun`          |  Blood Urea Nitrogen (BUN)            | numeric  | 4.0 - 174.0        | Blood Urea Nitrogen (BUN) in mg/dL |
|`alt`          |  Alanine Aminotransferase (ALT)       | numeric  | 2.0 - 929.0        | Alanine Aminotransferase (ALT) in U/L |
|`bili`         |  Total Bilirubin                      | numeric  | 0.0 - 5.0          | Total Bilirubin in mg/dL |
|`hemo`         |  CBC: Hemoglobin                      | numeric  | 6.0 - 19.0         | Hemoglobin in g/dL |
|`glyc`         |  Glycemia                             | numeric  | 57.0 - 620.0       | Blood Glucose in mg/dL |
|`pot`          |  Potassium Blood Level                | numeric  | 2.0 - 7.0          | Potassium Blood Level in mmol/L |
Categorical
|`gender`       | Gender                                | category | [0.0, 1.0]         | Select the gender of the patient. 0.0 -> male; 1.0 -> female |
Comorbitiites
|`dysrh`        | Cardiac dysrhythmias                  | boolean  | true/false         | Disease |
|`kidney`       | Chronic kidney disease                | boolean  | true/false         | Disease |
|`atheros`      | Coronary atherosclerosis and other heart disease| boolean  | true/false       | Disease |
|`diabetes`     | Diabetes                              | boolean  | true/false         | Disease |

