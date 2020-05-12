import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def get_page_desc_mortality(labs_auc,no_labs_auc):
    return [ \
        html.H2("Metodi analitici possono calcolare il rischio di mortalità"),
        html.Hr(),
        dcc.Markdown(
             """I pazienti in gravi condizioni a causa del virus COVID-19 necessitano di risorse ospedaliere disponibili in numero esiguo, \
             come ventilatori e letti di terapia intensiva. Quando il numero di pazienti è superiore alla quantità di risorse a disposizione, \
             i medici hanno la pesante responsabilità \
             di scegliere a quali pazienti dare priorità. Per aiutarli nel compiere una decisione fondata su basi matematiche, \
             abbiamo sviluppato un calcolatore di mortalità per pazienti ospidalizzati per COVID-19.
             """,
        ),
        dcc.Markdown(
             """ Abbiamo sviluppato due calcolatori che predicono **la probabilità che un paziente affetto da \
             COVID-19 ha di morire quando viene ospedalizzato:**"""),
        dcc.Markdown(
             """* Un calcolatore che utilizza dati anagrafici, valori vitali e comorbidità, ma **senza valori di laboratorio**. \
              Nella nostra visione, questo modello verrà usato nella fase di smistamento per un paziente affetto da COVID-19 che \
              va all'ospedale per determinare in modo preliminare la gravità della propria condizione di salute. \
              L'Area Sotto la Curva (AUC) su pazienti fuori dal campione di allenamento è {}.
             """.format(no_labs_auc),
        ),
        dcc.Markdown(
             """* Un calcolatore che utilizza dati anagrafici, valori vitali, comorbidità e **valori di laboratorio**. Questo punteggio di rischio può \
             essere utilizzato per la fase post smistamento per avere una stima più accurata e dettagliata della gravità della condizione \
             medica del paziente affetto da COVID-19. L'Area Sotto la Curva (AUC) su pazienti fuori dal campione di allenamento è {}.
             """.format(labs_auc),
        ),
        dcc.Markdown(
             """ **NOTA (Questa è una versione in fase di sviluppo!):** I modelli sono tanto accurati quanto i dati sui quali vengono allenati. Rilasceremo nuove versioni \
             del calcolatore quando riceveremo ulteriori dati dalle istituzioni con cui collaboriamo. Se una istituzione sanitaria volesse \
             contribuire al nostro lavoro, cortesemente ci contatti [qui](https://www.covidanalytics.io/contact).
             """,
        ),
    ]

page_desc_infection = [ \
            html.H2("Modelli analitici possono identificare pazienti infetti"),
            dcc.Markdown(
                 """I test per identificare pazienti affetti da COVID-19 impiegano tempo, sono costosi e necessitano che il paziente \
                 si presenti di persona al centro specializzato, aumentando la possibilità di essere esposto al virus. Per aiutare nell'identificazione \
                 di pazienti sintomatici, abbiamo sviluppato un calcolatore per predirre la probabilità che un paziente sia infetto. \
                 """,
            ),
            html.Hr(),
            dcc.Markdown(
                 """ **NOTA (Questa è una versione in fase di sviluppo!):** I modelli sono tanto accurati quanto i dati sui quali vengono allenati. Rilasceremo nuove versioni \
             del calcolatore quando riceveremo ulteriori dati dalle istituzioni con cui collaboriamo. Se una istituzione sanitaria volesse \
             contribuire al nostro lavoro, cortesemente ci contatti [qui](https://www.covidanalytics.io/contact).
             """,
            )
        ]

oxygen_text = ["Inserisci il valore.","Hai difficoltà respiratorie?"]

submit = "Invia"

insert_feat = 'Inserisci i valori seguenti nel calcolatore.'

results_card_mortality = "Il rischio di mortalità è:"
results_card_infection = ["Il rischio di infezione è:", " su 10"]

visual_1 = """Il [grafico SHAP](https://github.com/slundberg/shap) sottostante riassume l'effetto che ogni valore ha \
            sulla predizione di rischio. I valori in blue diminuiscono il rischio del paziente, \
            mentre quelli in rosso lo aumentano. L'effetto nella predizione è proporzionale alla larghezza della barra dei valori. \
            Più la barra è larga, maggiore è l'effetto del valore sulla predizione finale di rischio. \
            Nota: il sesso è rappresentato come un valore binario (0=Uomo, 1=Donna)."""

def get_model_desc_mortality(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        intro = dcc.Markdown(
             """
             Il nostro modello è stato allenato su {} pazienti (dei quali {}% deceduti) ospitalizzati per COVID-19 in: \
             """.format(labs_population[0],str(int(float(labs_positive[0])*100))),
        )
        auc = html.Div(
             [
             "Il calcolatore si basa sul ", html.A("classificatore XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "L'Area Sotto la Curva (AUC) su {} pazienti fuori dal campione di allenamento (dei quali {}% deceduti) è ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "Quando un valore è mancante, il calcolatore ne stima il valore e poi lo riporta in seguito."
             ]
        )
    else:
        intro = dcc.Markdown(
             """
             Il nostro modello è stato allenato su {} pazienti (dei quali {}% deceduti) ospitalizzati per COVID-19 in: \
             """.format(no_labs_population[0],str(int(float(no_labs_positive[0])*100))),
        )
        auc = html.Div(
            [
             "Il calcolatore si basa sul ", html.A("classificatore XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "L'Area Sotto la Curva (AUC) su {} pazienti fuori dal campione di allenamento (dei quali {}% deceduti) è ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(no_labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".", html.Br(),\
             "Quando un valore è mancante, il calcolatore ne stima il valore e poi lo riporta in seguito."
             ]
        )

    return [ \
        html.H2("Dettagli Tecnici"),
        intro,
        dcc.Markdown(
             """* La città di Cremona ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona è una delle città italiane più duramente colpite con diversi migliaia di casi ad oggi.""",
        ),
        dcc.Markdown(
             """* [Ospedali HM](https://www.fundacionhm.com/), un importante gruppo ospedaliero in Spagna con 15 ospedali e 21 centri \
             clinici che coprono le regioni di Madrid, Galicia e León. """,
        ),
        dcc.Markdown(
             """Date le caratteristiche della popolazione di cui abbiamo i dati, pensiamo che il nostro modello sia rilevante soprattutto per: (a) Popolazione occidentale; \
             (b) Pazienti in condizioni gravi; (c) Ospedali congestionati. """,
        ),
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """Utilizziamo [grafici SHAP](https://github.com/slundberg/shap) \
             per interpretare i modelli di XGBoost. I seguenti grafici SHAP riassumono l'effetto dei valori \
             per importanza e direzionalità. I valori sono ordinati in ordine decrescente di importanza, \
             con i più importanti in cima alla lista nel grafico. Per un dato valore, \
             la riga corrispondente mostra il grafico dell'impatto che il valore ha sulla predizione, con valori \
             in ordine dal più basso (blu) al più alto (rosso). Valori di SHAP più alti \
             corrispondono a una maggiore probabilità di avere il risultato selezionato (mortalità o \
             infezione). Quindi, quando i valori sono orientati da blu a rosso (guardando da sinistra a destra) \
             vuol dire che il rischio aumenta quando i valori aumentano, come per esempio accade con l'età. Quando invece i valori sono orientati \
             da rosso a blu, il rischio diminuisce quando il valore aumenta, come accade per la saturazione di ossigeno. \
             Nota: il sesso è rappresentato come un valore binario (0=Uomo, 1=Donna), quindi un valore "basso" di esso \
             corrisponde ad un paziente maschio."""),
        dcc.Markdown(
             """In generale, l'importanza dei valori inseriti nel calcolatore è la seguente:""",
        )
    ]

def get_model_desc_infection(labs,labs_auc,no_labs_auc,labs_population,no_labs_population,labs_positive,no_labs_positive):
    if labs:
        auc = html.Div(
             [
             "Il calcolatore si basa sul ", html.A("classificatore XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "L'Area Sotto la Curva (AUC) su {} pazienti fuori dal campione di allenamento (dei quali {}% infetti) è ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "Quando un valore è mancante, il calcolatore ne stima il valore e poi lo riporta in seguito."
             ]
        )
        desc = dcc.Markdown(
             """
             Il nostro modello è stato allenato su {} pazienti (dei quali {}% positivi al test di COVID-19) \
             che sono stati ricoverati nel reparto emergenze nell'ospedale della città italiana di Cremona \
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona è una delle città italiane più duramente colpite con diversi migliaia di casi ad oggi.
             """.format(labs_population[0],str(int(float(labs_positive[0])*100))),
        )
    else:
        auc = html.Div(
            [
             "Il calcolatore si basa sul ", html.A("classificatore XGBoost.",href = "https://xgboost.readthedocs.io/"), html.Br(),
             "L'Area Sotto la Curva (AUC) su {} pazienti fuori dal campione di allenamento (dei quali {}% infetti) è ".format(labs_population[1],str(int(float(labs_positive[1])*100))),
             html.Span(' {}'.format(no_labs_auc), style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "Quando un valore è mancante, il calcolatore ne stima il valore e poi lo riporta in seguito."
             ]
        )
        desc = dcc.Markdown(
             """
             Il nostro modello è stato allenato su {} pazienti (dei quali {}% positivi al test di COVID-19) \
             che sono stati ricoverati nel reparto emergenze nell'ospedale della città italiana di Cremona \
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona è una delle città italiane più duramente colpite con diversi migliaia di casi ad oggi.
             """.format(no_labs_population[0],str(int(float(no_labs_positive[0])*100))),
        )
    return [ \
        html.H2("Dettagli Tecnici"),
        desc,
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """Utilizziamo [grafici SHAP](https://github.com/slundberg/shap) \
             per interpretare i modelli di XGBoost. I seguenti grafici SHAP riassumono l'effetto dei valori \
             per importanza e direzionalità. I valori sono ordinati in ordine decrescente di importanza, \
             con i più importanti in cima alla lista nel grafico. Per un dato valore, \
             la riga corrispondente mostra il grafico dell'impatto che il valore ha sulla predizione, con valori \
             in ordine dal più basso (blu) al più alto (rosso). Valori di SHAP più alti \
             corrispondono a una maggiore probabilità di avere il risultato selezionato (mortalità o \
             infezione). Quindi, quando i valori sono orientati da blu a rosso (guardando da sinistra a destra) \
             vuol dire che il rischio aumenta quando i valori aumentano, come per esempio accade con l'età. Quando invece i valori sono orientati \
             da rosso a blu, il rischio diminuisce quando il valore aumenta, come accade per la saturazione di ossigeno. \
             Nota: il sesso è rappresentato come un valore binario (0=Uomo, 1=Donna), quindi un valore "basso" di esso \
             corrisponde ad un paziente maschio."""),
        dcc.Markdown(
             """In generale, l'importanza dei valori inseriti nel calcolatore è la seguente:""",
        )
    ]

feature_names = {
    'ABG: Oxygen Saturation (SaO2)': 'Saturazione Ossigeno',
    'Alanine Aminotransferase (ALT)': 'Alanina Aminotransferasi (ALT)',
    'Age': 'Età',
    'Aspartate Aminotransferase (AST)': 'Aspartato Aminotransferasi ',
    'Blood Creatinine': 'Creatinina',
    'Blood Sodium': 'Sodio',
    'Blood Urea Nitrogen (BUN)': 'Azoto Ureico Ematico (BUN)',
    'Body Temperature': 'Temperatura Corporea',
    'C-Reactive Protein (CRP)':  'Proteina C Reattiva (PCR)',
    'CBC: Hemoglobin': 'Emoglobina',
    'CBC: Leukocytes': 'Leucociti',
    'CBC: Mean Corpuscular Volume (MCV)': 'Volume Corpuscolare Medio',
    'CBC: Platelets': 'Piastrine',
    'CBC: Red cell Distribution Width (RDW)': 'Valore Distributivo Globuli Rossi',
    'Cardiac Frequency': 'Battito Cardiaco',
    'Cardiac dysrhythmias': 'Aritmia Cardiaca',
    'Gender' : 'Sesso',
    'Glycemia': 'Glucosio',
    'Potassium Blood Level': 'Potassio',
    'Prothrombin Time (INR)': 'Tempo Di Protrombina Ratio',
    'Systolic Blood Pressure': 'Pressione Sistolica',
    'SaO2': 'Saturazione Ossigeno',
    'Blood Calcium': 'Calcio',
    'ABG: PaO2': 'Pressione Parziale Arteriosa (PaO2)',
    'ABG: pH': 'PH Arterioso',
    'Cholinesterase': 'Colinesterasi',
    'Respiratory Frequency': 'Frequenza Respiratoria',
    'ABG: MetHb': 'Metaemoglobina',
    'Total Bilirubin': 'Bilirubina Totale',
    'Comorbidities':'Comorbidità',
    'Diabetes': 'Diabete',
    'Chronic kidney disease': 'Malattia Renale Cronica',
    'Coronary atherosclerosis and other heart disease': 'Aterosclerosi Coronarica'
}
