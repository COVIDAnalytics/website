import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def get_page_desc_mortality(labs_auc,no_labs_auc):
    return [ \
        html.H2("Analytics puede calcular el riesgo de mortalidad"),
        html.Hr(),
        dcc.Markdown(
             """Los pacientes graves con COVID-19 requieren los recursos de atención médica más escasos, \
             respiradores y camas de UCIs. Cuando el número de pacientes excede la \
             disponibilidad de estos recursos, los médicos tienen la difícil responsabilidad de\
             priorizar entre pacientes. Para ayudarlos a tomar una decisión informada, \
             desarrollamos la calculadora de mortalidad para pacientes ingresados con COVID-19.
             """,
        ),
        dcc.Markdown(
             """Hemos desarrollado dos calculadoras que predicen **la probabilidad de mortalidad de \
             un paciente con COVID-19 que llega a un hospital:**"""),
        dcc.Markdown(
             """* Una calculadora que utiliza datos demográficos, signos vitales y comorbilidades, \
             pero ** sin valores de laboratorio**. Prevemos que este modelo se utilizará en el momento \
             del triaje para un paciente con COVID-19 que llega al hospital para evaluar de manera \
             preliminar la gravedad de su afección. The out of sample AUC is {}.
             """.format(no_labs_auc),
        ),
        dcc.Markdown(
             """* Una calculadora que utiliza datos demográficos, signos vitales, comorbilidades y \
             ** valores de laboratorio**. Este puntaje de riesgo se puede usar después del triaje \
             para evaluar de manera más precisa y detallada la gravedad de la condición de un \
             paciente con COVID-19.The out of sample AUC is {}.
             """.format(labs_auc),
        ),
        dcc.Markdown(
             """ **NOTA (¡Esta es una versión de desarrollo!):** Los modelos son tan precisos como los \
             datos en los que están capacitados. Lanzaremos nuevas versiones de la calculadora a medida \
             que aumente la cantidad de datos que recibimos de nuestras instituciones asociadas. Si \
             usted es una institución médica y está dispuesto a contribuir a nuestro esfuerzo, \
             comuníquese con nosotros [aquí](https://www.covidanalytics.io/contact).
             """,
        ),
    ]

page_desc_infection = [ \
            html.H2("Analytics puede identificar pacientes infectados"),
            dcc.Markdown(
                 """Las pruebas COVID-19 requieren mucho tiempo, son caras y requieren que los pacientes \
                 visiten las instalaciones en persona, lo que aumenta la exposición al virus. Para ayudar \
                 a identificar pacientes sintomáticos, desarrollamos una calculadora basada en datos para \
                 predecir la probabilidad de infección.
                 """,
            ),
            html.Hr(),
            dcc.Markdown(
                 """ **NOTA (¡Esta es una versión de desarrollo!):** Los modelos son tan precisos como los \
                 datos en los que están capacitados. Lanzaremos nuevas versiones de la calculadora a medida \
                que aumente la cantidad de datos que recibimos de nuestras instituciones asociadas. Si \
                usted es una institución médica y está dispuesto a contribuir a nuestro esfuerzo, \
                comuníquese con nosotros [aquí](https://www.covidanalytics.io/contact).
                 """,
            )
        ]

oxygen_text = ["Inserte el valor.","¿Tienes dificultad para respirar?"]

submit = "Enviar"

insert_feat = 'Inserte las siguientes características en la calculadora de riesgos.'

results_card_mortality = "El puntaje de riesgo de mortalidad es:"
results_card_infection = ["El puntaje de riesgo de infección es:", " de 10"]

visual_1 = "explicación"

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
             """.format(no_labs_population[1],str(int(float(no_labs_positive[1])*100))),
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
        html.H2("Detalles Técnicos"),
        intro,
        dcc.Markdown(
             """* La ciudad italiana de Cremona ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona es una de las provincias italianas más afectadas en Lombardía con varios miles de casos positivos hasta la fecha.""",
        ),
        dcc.Markdown(
             """* [HM Hospitals](https://www.fundacionhm.com/), un grupo hospitalario líder en España con 15 hospitales generales y 21 \
             centros clínicos que cubren las regiones de Madrid, Galicia y León. """,
        ),
        dcc.Markdown(
             """ Dada nuestra población en formación, estamos más seguros de la relevancia de nuestro modelo para: (a) la población occidental; \
             (b) pacientes severos a agudos; (c) Hospitales congestionados. """,
        ),
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """En general, la importancia de las características del modelo es la siguiente:""",
        )
    ]

def get_model_desc_infection(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        auc = html.Div(
             [
             "The calculator is based on ", html.A("XGBoost classifier.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "After predicting the risk using the binary classification model, we cluster its predictions in three classes \
             of risk (low/medium/high) to calibrate its output for the general population.", html.Br(),
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
             "After predicting the risk using the binary classification model, we cluster its predictions in three classes \
             of risk (low/medium/high) to calibrate its output for the general population.", html.Br(),
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
             """Overall, the importance of the features is as follows:""",
        )
    ]

feature_names = {
    'ABG: Oxygen Saturation (SaO2)': 'Oxygen Saturation',
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
    'CBC: Red cell Distribution Width (RDW)': 'Red Cell Distribution Width (RDW)',
    'Cardiac Frequency': 'Heart Rate',
    'Cardiac dysrhythmias': 'Cardiac dysrhythmias',
    'Gender' : 'Gender',
    'Glycemia': 'Glycemia',
    'Potassium Blood Level': 'Potassium',
    'Prothrombin Time (INR)': 'Prothrombin Time',
    'Systolic Blood Pressure': 'Systolic Blood Pressure (SYS)',
    'SaO2': 'Oxygen Saturation',
    'Blood Calcium': 'Calcium',
    'ABG: PaO2': 'Partial Pressure Oxygen (PaO2)',
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
