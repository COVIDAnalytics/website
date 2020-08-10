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
| Parameter | Description |
| --------  | ----------- | 
| `age` | Age |
| `sao2-labs` | ABG: Oxygen Saturation (SaO2) |
| `sao2-nolabs` | SaO2 |
| `cardiac_freq` | Cardiac Frequency |
| `alt` | Alanine Aminotransferase (ALT) |
| `creat` | Blood Creatinine |
| `sodium` | Blood Sodium |
| `bun` | Blood Urea Nitrogen (BUN) |
| `temp` | Body Temperature |
| `crp` | C-Reactive Protein (CRP) |
| `hemo` | CBC: Hemoglobin |
| `leuko` | CBC: Leukocytes |
| `mcv` | CBC: Mean Corpuscular Volume (MCV) |
| `ast` | Aspartate Aminotransferase (AST) |
| `platel` | CBC: Platelets |
| `glyc` | Glycemia |
| `pot` | Potassium Blood Level |
| `inr` | Prothrombin Time (INR) |
| `gender` | Gender |
| `dysrh` | Cardiac dysrhythmias |
| `kidney` | Chronic kidney disease |
| `atheros` | Coronary atherosclerosis and other heart disease |
| `diabetes` | Diabetes |
| `bili` | Total Bilirubin |
| `rdw` | CBC: Red cell Distribution Width (RDW) |
| `resp_freq` | Respiratory Frequency |
| `calcium` | Blood Calcium |

