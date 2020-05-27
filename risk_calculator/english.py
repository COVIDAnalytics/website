import dash_core_components as dcc
import dash_html_components as html

def get_page_desc_mortality(labs_auc,no_labs_auc):
    return [ \
        html.H2("Analytics can calculate the risk of mortality"),
        html.Hr(),
        dcc.Markdown(
             """ Severe COVID-19 patients require the most scarce health care resources, \
             ventilators and intensive care beds. When the number of patients exceeds the \
             availability of these resources, physicians have the difficult responsibility \
             to prioritize between patients. To help them make an informed decision, we \
             developed the mortality calculator for admitted COVID-19 patients.
             """,
        ),
        dcc.Markdown(
             """ We have developed two calculators that predict **the probability of mortality \
             of a COVID-19 patient who arrives at a hospital:**"""),
        dcc.Markdown(
             """* A calculator that uses demographics, vitals and comorbidities, but **without lab values**. \
              We envision that this model will be used at the time of triage for a COVID-19 patient who \
              arrives at the hospital to assess in a preliminary way the severity of his or her condition. \
              The out of sample AUC is {}.
             """.format(no_labs_auc),
        ),
        dcc.Markdown(
             """* A calculator that uses demographics, vitals, comorbidities and **lab values**. This risk score can \
             be used post-triage to assess in a more accurate and detailed way the severity of a COVID-19 \
             patient’s condition. The out of sample AUC is {}.
             """.format(labs_auc),
        ),
        dcc.Markdown(
             """ Models are only as good as the data they are trained on. We will release new versions of \
             the calculator as the amount of data we receive from our partner institutions increases. If you \
             are a medical institution and are willing to contribute to our effort, please reach out to \
             us [here](https://www.covidanalytics.io/contact).
             """,
        ),
    ]

def get_page_desc_infection():
    return [ \
            html.H2("Analytics can identify infected patients"),
            dcc.Markdown(
                 """COVID-19 tests are time consuming, expensive and require patients to visit \
                 facilities in person, increasing exposure to the virus. To help identifying \
                 symptomatic patients, we developed a data-driven calculator to predict the \
                 probability of being infected.
                 """,
            ),
            html.Hr(),
            dcc.Markdown(
                 """ **NOTE (This is a developmental version!):** A model is only as good as the \
                 data it is trained on. We will release new versions of the calculator as the \
                 amount of data we receive from our partner institutions increases. If you are a \
                 medical institution and are willing to contribute to our effort, please reach out \
                 to us [here](https://www.covidanalytics.io/contact).
                 """,
            )
        ]

def get_oxygen_text():
    return ["Insert the value.","Do you have shortness of breath?"]

submit = "Submit"

def get_insert_feat():
    return 'Insert the features below into the risk calculator.'

def get_results_card_mortality():
    return "The mortality risk score is:"

def get_results_card_infection():
    return ["The infection risk score is:", " out of 10"]

def get_visual_1():
    return """The [SHAP plot](https://github.com/slundberg/shap) below summarizes the individual feature \
            contributions to the risk score. Features in blue decrease risk from the population baseline, \
            whereas features in red increase risk. The contribution is proportional to the width of the feature's \
            bar. Wider bars have higher importance in the final risk score. \
            Note: gender is encoded as a binary value (0=Male, 1=Female)."""

def get_model_desc_mortality(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        intro = dcc.Markdown(
             """
             Our model was trained on {} patients (out of whom {}% deceased) hospitalized due to COVID-19 in: \
             """.format(labs_population[0],str(int(float(labs_positive[0])*100))),
        )
        auc = html.Div(
             [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "The out of sample area under the curve (AUC) on {} patients (out of whom {}% deceased) is ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )
    else:
        intro = dcc.Markdown(
             """
             Our model was trained on {} patients (out of whom {}% deceased) hospitalized due to COVID-19 in: \
             """.format(no_labs_population[0],str(int(float(no_labs_positive[0])*100))),
        )
        auc = html.Div(
            [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "The out of sample area under the curve (AUC) on {} patients (out of whom {}% deceased) is ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(no_labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )

    return [ \
        html.H2("Technical details"),
        intro,
        dcc.Markdown(
             """* The Italian city of Cremona ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona is one of the most severely hit italian provinces in Lombardy with several thousand positive cases to date.""",
        ),
        dcc.Markdown(
             """* [HM Hospitals](https://www.fundacionhm.com/), a leading Hospital Group in Spain with 15 general hospitals and 21 clinical \
             centres that cover the regions of Madrid, Galicia, and León. """,
        ),
        dcc.Markdown(
             """* [Hartford HealthCare](https://hartfordhealthcare.org), a major hospital network serving patients throughout Connecticut (USA). """,
        ),
        dcc.Markdown(
             """Given our training population, we are most confident about the relevance of our model to: (a) Western population; \
             (b) Severe to acute patients; (c) Congested hospitals. """,
        ),
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """We use [SHAP plots](https://github.com/slundberg/shap) \
             to interpret the XGBoost models. The SHAP plot below summarizes features by \
             their importance and directionality. Features are ordered by decreasing significance, \
             with the most important feature listed at the top of the plot. For a given feature, \
             the corresponnding row shows a plot of the feature's impact on the prediction as the \
             value ranges from its lowest (blue) to highest (red) value. Higher SHAP values \
             correspond to increased likelihood of having a positive outcome (i.e. mortality or \
             infection). Thus, features with the color scale oriented blue to red (moving left to \
             right) have increasing risk as the feature increases, such as Age. Features oriented \
             red to blue have decreasing risk as the feature increases, such as Oxygen Saturation. \
             Note: gender is encoded as a binary value (0=Male, 1=Female), so "lower" values of gender \
             correspond to male patients."""),
        dcc.Markdown("""Overall, the importance of the top features is as follows:"""),
    ]

def get_model_desc_infection(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        auc = html.Div(
             [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "The out of sample area under the curve (AUC) on {} patients (out of whom {}% infected) is ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )
        desc = dcc.Markdown(
             """
             Our model was trained on {} patients (out of whom {}% COVID-19 positive) \
             who visited the emergency room in the italian city of Cremona \
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona is one of the most severely hit italian provinces in Lombardy with several thousand \
             positive cases to date.
             """.format(labs_population[0],str(int(float(labs_positive[0])*100))),
        )
    else:
        auc = html.Div(
            [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "The out of sample area under the curve (AUC) on {} patients (out of whom {}% infected) is ".format(no_labs_population[1],str(int(float(no_labs_positive[1])*100))),
             html.Span(' {}'.format(no_labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )
        desc = dcc.Markdown(
             """
             Our model was trained on {} patients (out of whom {}% COVID-19 positive) \
             who visited the emergency room in the italian city of Cremona \
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona is one of the most severely hit italian provinces in Lombardy with several thousand \
             positive cases to date.
             """.format(no_labs_population[0],str(int(float(no_labs_positive[0])*100))),
        )
    return [ \
        html.H2("Technical details"),
        desc,
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """We use [SHAP plots](https://github.com/slundberg/shap) \
             to interpret the XGBoost models. The SHAP plot below summarizes features by \
             their importance and directionality. Features are ordered by decreasing significance, \
             with the most important feature listed at the top of the plot. For a given feature, \
             the corresponnding row shows a plot of the feature's impact on the prediction as the \
             value ranges from its lowest (blue) to highest (red) value. Higher SHAP values \
             correspond to increased likelihood of having a positive outcome (i.e. mortality or \
             infection). Thus, features with the color scale oriented blue to red (moving left to \
             right) have increasing risk as the feature increases, such as Age. Features oriented \
             red to blue have decreasing risk as the feature increases, such as Oxygen Saturation. \
             Note: gender is encoded as a binary value (0=Male, 1=Female), so "lower" values of gender \
             correspond to male patients."""),
        dcc.Markdown("""Overall, the importance of the top features is as follows:"""),
    ]

def get_feature_names():
        return {
        'ABG: Oxygen Saturation (SaO2)': 'Oxygen Saturation',
        'Alanine Aminotransferase (ALT)': 'Alanine Aminotransferase',
        'Age': 'Age',
        'Aspartate Aminotransferase (AST)': 'Aspartate Aminotransferase',
        'Blood Creatinine': 'Creatinine',
        'Blood Sodium': 'Sodium',
        'Blood Urea Nitrogen (BUN)': 'Blood Urea Nitrogen',
        'Body Temperature': 'Temperature',
        'C-Reactive Protein (CRP)':  'C-Reactive Protein',
        'CBC: Hemoglobin': 'Hemoglobin',
        'CBC: Leukocytes': 'Leukocytes',
        'CBC: Mean Corpuscular Volume (MCV)': 'Mean Corpuscular Volume',
        'CBC: Platelets': 'Platelets',
        'CBC: Red cell Distribution Width (RDW)': 'Red Cell Distribution Width',
        'Cardiac Frequency': 'Heart Rate',
        'Cardiac dysrhythmias': 'Cardiac dysrhythmias',
        'Gender' : 'Gender',
        'Glycemia': 'Blood Glucose',
        'Potassium Blood Level': 'Potassium',
        'Prothrombin Time (INR)': 'Prothrombin Time',
        'Systolic Blood Pressure': 'Systolic Blood Pressure',
        'SaO2': 'Oxygen Saturation',
        'Blood Calcium': 'Calcium',
        'ABG: PaO2': 'Partial Pressure Oxygen',
        'ABG: pH': 'Arterial Blood Gas pH',
        'Cholinesterase': 'Cholinesterase',
        'Respiratory Frequency': 'Respiratory Frequency',
        'ABG: MetHb': 'Arterial Blood Gas Methemoglobinemia',
        'Total Bilirubin': 'Total Bilirubin',
        'Comorbidities':'Comorbidities',
        'Diabetes': 'Diabetes',
        'Chronic kidney disease': 'Chronic kidney disease',
        'Cardiac dysrhythmias': 'Cardiac dysrhythmias',
        'Coronary atherosclerosis and other heart disease': 'Coronary atherosclerosis and other heart disease'
    }
