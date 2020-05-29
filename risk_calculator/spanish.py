import dash_core_components as dcc
import dash_html_components as html

def get_page_desc_mortality(labs_auc,no_labs_auc):
    return [ \
        html.H2("Analytics puede calcular el riesgo de mortalidad"),
        html.Hr(),
        dcc.Markdown(
             """Los pacientes con COVID-19 en situación grave requieren los recursos de atención médica más escasos, \
             respiradores y camas de UCIs. Cuando el número de pacientes excede la \
             disponibilidad de estos recursos, los médicos tienen la dura responsabilidad de\
             priorizar entre pacientes. Para ayudarlos a tomar una decisión informada, \
             desarrollamos la calculadora de mortalidad para pacientes que estan ingresados con COVID-19.
             """,
        ),
        dcc.Markdown(
             """Hemos desarrollado dos calculadoras que predicen **la probabilidad de mortalidad para \
             un paciente que esta hospitalizado con COVID-19:**"""),
        dcc.Markdown(
             """* Una calculadora que utiliza datos demográficos, signos vitales, comorbilidades y \
             ** valores de laboratorio**. Este puntaje de riesgo se puede usar después del triaje \
             para evaluar de manera más precisa y detallada la gravedad de la condición de un \
             paciente con COVID-19. El área bajo la curva (AUC) en predicciones fuera de muestra es {}.
             """.format(labs_auc),
        ),
        dcc.Markdown(
             """* Una calculadora que utiliza datos demográficos, signos vitales y comorbilidades, \
             pero **sin valores de laboratorio**. Prevemos que este modelo se utilizará para evaluar de manera \
             preliminar la gravedad de un paciente con COVID-19 en el momento \
             del triaje cuando llega al hospital. El área bajo la curva (AUC) en predicciones fuera de muestra es {}.
             """.format(no_labs_auc),
        ),
        dcc.Markdown(
             """ **NOTA (¡Esta es una versión de desarrollo!):** La precisión de los modelos depende \
             de la calidad de los datos con los que han sido creados. Lanzaremos nuevas versiones de la calculadora a medida \
             que aumente la cantidad de datos que recibamos de nuestras instituciones asociadas. Si \
             usted es una institución médica y está dispuesto a contribuir a nuestro esfuerzo, \
             comuníquese con nosotros [aquí](https://www.covidanalytics.io/contact).
             """,
        ),
    ]

def get_page_desc_infection():
    return [ \
            html.H2("Analytics puede identificar pacientes infectados"),
            dcc.Markdown(
                 """Las pruebas para detectar el COVID-19 requieren mucho tiempo, son caras y requieren que los pacientes \
                 visiten las instalaciones en persona, lo que aumenta la exposición al virus. Para ayudar \
                 a identificar pacientes sintomáticos, desarrollamos una calculadora basada en datos para \
                 predecir la probabilidad de infección.
                 """,
            ),
            html.Hr(),
            dcc.Markdown(
                 """ **NOTA (¡Esta es una versión de desarrollo!):** Los modelos son tan precisos como los \
                 datos en los que están capacitados. Lanzaremos nuevas versiones de la calculadora a medida \
                que aumente la cantidad de datos que recibamos de nuestras instituciones asociadas. Si \
                usted es una institución médica y está dispuesto a contribuir a nuestro esfuerzo, \
                comuníquese con nosotros [aquí](https://www.covidanalytics.io/contact).
                 """,
            )
        ]

def get_oxygen_text():
    return ["Inserte el valor.","¿Tienes dificultad para respirar?"]

submit = "Enviar"

def get_insert_feat():
    return 'Inserte las siguientes características en la calculadora de riesgos.'

def get_results_card_mortality():
    return "El puntaje de riesgo de mortalidad es:"

def get_results_card_infection():
    return ["El puntaje de riesgo de infección es:", " de 10"]

def get_visual_1():
    return """El siguiente [gráfico de SHAP](https://github.com/slundberg/shap) resume como cada característica \
            contribuye al puntaje de riesgo. Las características en azul bajan el riesgo, \
            mientras las características en rojo las aumentan. La contribución de cada característica es proporcional al ancho de la \
            barra. Las barras más anchas tienen mayor importancia en el puntaje de riesgo final. \
            Nota: el género se codifica como un valor binario (0 = Masculino, 1 = Femenino)."""

def get_model_desc_mortality(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        intro = dcc.Markdown(
             """
             Nuestro modelo ha sido creado usando datos de {} pacientes (de los cuales {}% fallecidos) hospitalizados debido a COVID-19 en: \
             """.format(labs_population[0],str(int(float(labs_positive[0])*100))),
        )
        auc = html.Div(
             [
             "La calculadora se basa en ", html.A("el clasificador XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "El área bajo la curva (AUC) para predicciones fuera de muestra con {} pacientes (de cuales {}% fueron falleciron) es ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "Si el usuario no dispone de información sobre todas las variables, nuestra calculadora les imputará un valor e informará al usuario del mismo."
             ]
        )
    else:
        intro = dcc.Markdown(
             """
             Nuestro modelo ha sido creado usando datos de {} pacientes (de los cuales {}% fallecidos) hospitalizados debido a COVID-19 en: \
             """.format(no_labs_population[0],str(int(float(no_labs_positive[0])*100))),
        )
        auc = html.Div(
            [
             "La calculadora se basa en ", html.A("el clasificador XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "El área bajo la curva (AUC) para predicciones fuera de muestra con {} pacientes (de cuales {}% fueron falleciron) es ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(no_labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "Si el usuario no dispone de información sobre todas las variables, nuestra calculadora les imputará un valor e informará al usuario del mismo."
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
             """ Dada la demografía de nuestra base de datos, consideramos que nuestro modelo tiene mayor relevancia en: (a) la población occidental; \
             (b) pacientes severos a agudos; (c) hospitales congestionados. """,
        ),
        html.Hr(),
        auc,
        html.Br(),
                dcc.Markdown(
             """ Utilizamos [gráficos de SHAP](https://github.com/slundberg/shap) \
             para la interpretación de los modelos de XGBoost. El diagrama SHAP que presentamos a continuación \
             resume las características basándose en su importancia y direccionalidad. Dichas \
             características aparecen ordenadas en orden de importancia decreciente, siendo \
             la primera la más relevante. \
             El gráfico muestra, para cada característica, el impacto de ésta en el modelo. Para ello, todas las observaciones de dicha característica
             se distribuyen horizontalmente en función de su valor de SHAP. El valor de SHAP cuantifica el impacto de cada observación
             en el resultado del modelo, siendo los valores indicadores de una mayor probabilidad de resultado positivo (mortalidad o infección en nuestro caso) y viceversa. Asimismo, \
             cada observación se colorea en función del valor relativo de dicha observación dentro del conjunto de la característica,
             siendo el azul asignado al valor más bajo y el rojo al más alto. Tomando como ejemplo la edad, se puede observar que
             el color varía de azul a rojo a medida que el valor SHAP aumenta. Esto indíca que el riesgo de mortalidad o infección ese mayor en la población de mayor edad. \
             En cambio, la evolución del color en el caso de la saturación de oxígeno es a la inversa, lo que indica que \
             son los niveles bajos de saturación los que conllevan mayor riesgo. Nota: el género se \
             codifica como un valor binario (0 = Masculino, 1 = Femenino), por lo \
             que los valores "menores" de género corresponden a pacientes masculinos."""),
        dcc.Markdown(
             """En general, la importancia de las características del modelo es la siguiente:""",
        )
    ]

def get_model_desc_infection(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        auc = html.Div(
             [
             "La calculadora se basa en", html.A("el clasificador XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "El área bajo la curva (AUC) para predicciones fuera de muestra con {} pacientes (de cuales {}% fueron infectados) es ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "Cuando faltan características, la calculadora imputará y informará sus valores."
             ]
        )
        desc = dcc.Markdown(
             """
             Nuestro modelo ha sido creado usando datos de {} pacientes (de los cuales {}% COVID-19 positivo) \
             que visitaron la sala de urgencias en la ciudad italiana de Cremona\
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona es una de las provincias italianas más afectadas en Lombardía con varios miles \
             de casos positivos hasta la fecha.
             """.format(labs_population[0],str(int(float(labs_positive[0])*100))),
        )
    else:
        auc = html.Div(
            [
             "La calculadora se basa en", html.A("el clasificador XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "El área bajo la curva (AUC) para predicciones fuera de muestra con {} pacientes (de cuales {}% fueron infectados) es ".format(no_labs_population[1],str(int(float(no_labs_positive[1])*100))),
             html.Span(' {}'.format(no_labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "Cuando faltan características, la calculadora imputará y informará sus valores."
             ]
        )
        desc = dcc.Markdown(
             """
             Nuestro modelo ha sido creado usando datos de {} pacientes (de los cuales {}% COVID-19 positivo) \
             que visitaron la sala de urgencias en la ciudad italiana de Cremona\
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona es una de las provincias italianas más afectadas en Lombardía con varios miles \
             de casos positivos hasta la fecha.
             """.format(no_labs_population[0],str(int(float(no_labs_positive[0])*100))),
        )
    return [ \
        html.H2("Detalles Técnicos"),
        desc,
        html.Hr(),
        auc,
        html.Br(),
                dcc.Markdown(
             """ Utilizamos [gráficos de SHAP](https://github.com/slundberg/shap) \
             para la interpretación de los modelos de XGBoost. El diagrama SHAP que presentamos a continuación \
             resume las características basándose en su importancia y direccionalidad. Dichas \
             características aparecen ordenadas en orden de importancia decreciente, siendo \
             la primera la más relevante. \
             El gráfico muestra, para cada característica, el impacto de ésta en el modelo. Para ello, todas las observaciones de dicha característica
             se distribuyen horizontalmente en función de su valor de SHAP. El valor de SHAP cuantifica el impacto de cada observación
             en el resultado del modelo, siendo los valores indicadores de una mayor probabilidad de resultado positivo (mortalidad o infección en nuestro caso) y viceversa. Asimismo, \
             cada observación se colorea en función del valor relativo de dicha observación dentro del conjunto de la característica,
             siendo el azul asignado al valor más bajo y el rojo al más alto. Tomando como ejemplo la edad, se puede observar que
             el color varía de azul a rojo a medida que el valor SHAP aumenta. Esto indíca que el riesgo de mortalidad o infección ese mayor en la población de mayor edad. \
             En cambio, la evolución del color en el caso de la saturación de oxígeno es a la inversa, lo que indica que \
             son los niveles bajos de saturación los que conllevan mayor riesgo. Nota: el género se \
             codifica como un valor binario (0 = Masculino, 1 = Femenino), por lo \
             que los valores "menores" de género corresponden a pacientes masculinos."""),
        dcc.Markdown(
             """En general, la importancia de las características mas importantes del modelo es la siguiente:""",
        )
    ]

def get_feature_names():
    return {
        'ABG: Oxygen Saturation (SaO2)': 'Saturación de oxígeno',
        'Alanine Aminotransferase (ALT)': 'Alanina aminotransferasa (ALT)',
        'Age': 'Edad',
        'Aspartate Aminotransferase (AST)': 'Aspartato aminotransferasa (AST)',
        'Blood Creatinine': 'Creatinina',
        'Blood Sodium': 'Sodio',
        'Blood Urea Nitrogen (BUN)': 'Nitrógeno ureico en sangre (BUN)',
        'Body Temperature': 'Temperatura',
        'C-Reactive Protein (CRP)':  'Proteína C-reactiva',
        'CBC: Hemoglobin': 'Hemoglobina',
        'CBC: Leukocytes': 'Leucocitos',
        'CBC: Mean Corpuscular Volume (MCV)': 'Volumen Corpuscular Promedio',
        'CBC: Platelets': 'Plaquetas',
        'CBC: Red cell Distribution Width (RDW)': 'Ancho de Distribución de Glóbulos Rojos',
        'Cardiac Frequency': 'Ritmo cardiaco',
        'Cardiac dysrhythmias': 'Disritmias cardíacas',
        'Gender' : 'Género',
        'Glycemia': 'Glucosa en Sangre',
        'Potassium Blood Level': 'Potasio',
        'Prothrombin Time (INR)': 'Tiempo de Protrombina',
        'Systolic Blood Pressure': 'Presión Arterial Sistólica',
        'SaO2': 'Saturación de oxígeno',
        'Blood Calcium': 'Calcio',
        'ABG: PaO2': 'Presión parcial de Oxígeno (PaO2)',
        'ABG: pH': 'pH por Gasometría Arterial',
        'Cholinesterase': 'Colinesterasa',
        'Respiratory Frequency': 'Frecuencia respiratoria',
        'ABG: MetHb': 'Metahemoglobinemia por Gasometría Arterial',
        'Total Bilirubin': 'Bilirrubina Total',
        'Comorbidities':'Comorbilidades',
        'Diabetes': 'Diabetes',
        'Chronic kidney disease': 'Enfermedad renal crónica',
        'Cardiac dysrhythmias': 'Disritmias cardíacas',
        'Coronary atherosclerosis and other heart disease': 'Aterosclerosis coronaria y otras enfermedades del corazón'
    }
