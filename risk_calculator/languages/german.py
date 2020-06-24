import dash_core_components as dcc
import dash_html_components as html

submit = "Senden"
missingFeatureTxt = "Die fehlende Charakteristik, {}, wurde ersetzt mit {}."
hasLabValues = "Haben Sie Laborwerte?"
notEnoughValues = "Bitte geben Sie mindestens {} numerische Werte ein."
outOfRangeValues = "Bitte geben Sie einen numerischen Wert zwischen {1} und {2} für die Charakteristik {0}"
hasO2Value = "Haben Sie einen SpO2- oder SaO2-Wert?"

def prompt_missing_feature(feature):
    return "Bitte geben Sie einen Wert für {} ein.".format(get_feature_names()[feature])


def get_yes(yes=True):
    return "Ja" if yes else "Nein"


def get_gender(male=True):
    return "Männlich" if male else "Weiblich"


def get_page_desc_mortality(labs_auc, no_labs_auc):
    return [
        html.H2("Datenanlyze kann das Sterblichkeitsrisiko errechnen"),
        html.Hr(),
        dcc.Markdown(
            """ COVID-19 Patienten die im kritischen Zustand sind brauchen die am knappsten \
            Gesundheitsversorgungsmittel, etwa Ventilatoren und Krankenbetten. Sobald allerdings die Zahl \
            der Patienten die Verfügbarkeit solcher Mittel ueberschreitet, müssen Ärtze schwere entschedungen \
            treffen und Patienten priorisieren. Um ihnen zu helfen informierte Entscheidungen zu treffen, \
            haben wir einen Sterblichkeitsrisikorechner für COVID-19 Patienten entwickelt.  
            """,
        ),
        dcc.Markdown(
            """ Wir haben zwei Rechner entwickelt die **die Todeswahrscheinlichkeit eines im Krankenhaus \
              aufgenommenen COVID-19 Patienten** einschäzen."""),
        dcc.Markdown(
            """* Einen Rechner der demographische Informationen, Vitalparameter, Komorbiditäten, und **Laborwerte** \
            verwendet. Der errechnete Risikowert kann nach der Erstaufnahme benutzt werden um die Schwere des \
            Zustandes eines COVID-19 Patienten genauer zu beurteilen. \
            Die Fläche unter der Kurve (AUC) von Vorhersagungen außerhalb der Stichproben ist {}.
            """.format(labs_auc),
        ),
        dcc.Markdown(
            """* Einen Rechner der demographische Informationen, Vitalparameter, Komorbiditäten \
             **aber keine Laborwerte** verwendet. Wir stellen uns vor, das dieses Modell während der Erstaufnahme \
             eines COVID-19 Patienten die Schwere seines Zustandes vorläufig einschätzten wird. \
             Die Fläche unter der Kurve (AUC) von Vorhersagungen außerhalb der Stichproben ist {}.
             """.format(no_labs_auc),
        ),
        dcc.Markdown(
            """Rechenmodelle sind nur so gut wie ihre Trainingsdaten. Als die Menge der vorhandenen Daten von \
             unseren Partnerinstiutionen zunimmnt, werden wir neue Versionen von unseren Rechnern veröffentlichen. \
             Falls Sie angehörig einer medizinischen Einrichtung sind und bereit sind einen Beitrag zu unserem Projekt \
             zu leisten, bitte kontaktieren Sie uns [hier](https://www.covidanalytics.io/contact).
             """,
        ),
    ]


def get_page_desc_infection():
    return [
        html.H2("Datenanalyze kann infizierte Patienten identifizieren"),
        dcc.Markdown(
            """COVID-19 Tests sind zeitaufwändig, teuer und erfordern, dass Patienten Einrichtungen persönlich \
                 besuchen, wodurch sie möglicherweise dem Virus ausgesetzt werden können. Um symptomatische Patienten \
                 zu helfen, haben wir einen datengesteurten Rechner entwickelt der die Warscheinlichkeit \
                 einer infektion abschätzt.
                 """,
        ),
        html.Hr(),
        dcc.Markdown(
            """ **HINWEIS (Dies ist eine Entwicklungsversion!):** Rechenmodelle sind nur so gut wie ihre \
                 Trainingsdaten. Als die Menge der vorhandenen Daten von unserern Partnerinstiutionen zunimmnt, \
                 werden wir neue Versionen von unseren Rechnern veröffentlichen. Falls Sie angehörig einer \
                 medizinischen Einrichtung sind und bereit sind einen Beitrag zu unserem Projekt zu leisten, \
                 bitte kontaktieren Sie uns [hier](https://www.covidanalytics.io/contact).
                 """,
        )
    ]


def get_oxygen_text():
    return ["Geben sie den Wert ein.", "Haben sie Kurzatmigkeit?"]


def get_insert_feat():
    return 'Fügen sie die Werte in den Risiko-Rechner ein.'


def get_results_card_mortality():
    return "Das Sterblichkeitsrisiko ist:"


def get_results_card_infection():
    return ["Der Infektionsrisikowert ist:", " aus 10"]


def get_visual_1():
    return """Die [SHAP Grafik](https://github.com/slundberg/shap) unten fasst zusammen wie individuelle \
            Charakteristiken zum Risikowert beitragen. Charakteristiken in blau verringern Risiko, \
            wohingegen Charakteristiken in rot Risiko erhöhen. Der Beitrag ist proportional zu der breite \
            der Charakteristikenleiste. Breitere Leisten haben einen größeren Einfluss auf den Endwert. \
            Hinweis: Das Geschlecht ist als Binärwert enkodiert (0=Männlich, 1=Weiblich)."""


def get_model_desc_mortality(auc, pop, pos):
    return [
        html.H2("Technische Details"),
        dcc.Markdown(
            """
             Durch diese Quellen, wurde unser Rechenmodell mit Daten von {} COVID-19 betroffenen Patienten \
             (von denen {}% starben) trainiert: \
             """.format(pop[0], str(int(float(pos[0]) * 100))),
        ),
        dcc.Markdown(
            """* Die Italienisch Stadt Cremona ([Azienda Socio-Sanitaria Territoriale di Cremona]\
            (https://www.asst-cremona.it/en/home)). Cremona ist mit mehreren tausend positiven Fällen eine \
            der am stärksten betroffenen italienischen Provinzen in der Lombardei.""",
        ),
        dcc.Markdown(
            """* [HM Hospitals](https://www.fundacionhm.com/), eine führende Gruppe aus Spanien mit 15 \
             Allgemeinkrankenhäusern und 21 klinischen Zentren in den Regionen Madrid, Galicia, und León. """,
        ),
        dcc.Markdown(
            """* [Hartford HealthCare](https://hartfordhealthcare.org), ein Krankenhausnetzwerk das \
            Patienten in ganz Connecticut (USA) abdeckt. """,
        ),
        dcc.Markdown(
            """Angesichts unseren Datenquellen, treffen unsere Modelle mehr auf die folgenden zu: \
             (a) Westliche bevölkerungen; \
             (b) Schwere bis akute Patienten; (c) Überlastete Krankenhäuser. """,
        ),
        html.Hr(),
        html.Div(
            [
                "Das Rechenmodell basiert auf ",
                html.A("den XGBoost Klassifikator.", href="https://xgboost.readthedocs.io/"),
                html.Br(),
                "Die Fläche unter der Kurve (AUC) von Vorhersagungen außerhalb der Stichproben von {} \
                Patienten (von denen {}% starben) ist ".format(pop[1], str(int(float(pos[1]) * 100))),
                html.Span(' {}'.format(auc), style={'color': '#800020', "fontWeight": "bold"}), ".", html.Br(),
                "Wenn Eingabewerte fehlen, shreibt der Rechner seine eigenen Werte zu und zeigt sie an."
            ]
        ),
        html.Br(),
        dcc.Markdown(
            """Wir nutzen [SHAP Graphen](https://github.com/slundberg/shap) \
             um unsere XGBoost Modelle zu interpretieren. Die SHAP Grafik unten fasst Charakteristiken nach \
             ihrer Wichtigkeit und Direktionalität zusammen. Die Charakteristiken werden nach abnehmender Wichtigkeit \
             sortiert, mit der wichtigsten Charakteristik oben. Für eine gegeben Charakteristik zeigt die \
             korrespondierende Grafik wie stark der Einfluß der Charakteristik auf das Endergebniss ist, mit rot \
             als größter Einfluss und blau als kleinster. Höhere SHAP Werte entsprechen erhöhten Wahrscheinlichkeiten \
             eines positiven Endergebnisses (z.B. Todeswahrscheinlichkeit oder Infektionswahrscheinlichkeit). \
             Daher, Charakteristiken mit dem Farbverlauf von blau zu rot (von links nach rechts) haben einen \
             erhöhten Risikowert wenn die Charakteristik steigt, sowie mit Alter. Charakteristiken die von rot \
             zu blau verlaufen, haben einen niedrigeren Risikowert wenn die Charakteristik steigt, sowie mit \
             Sauerstoffsättigung. Hinweis: Geschlecht wird als Binärwert enkodiert (0=Männlich, 1=Weiblich), \
             sodass "niedrigere" Geschlechtswerte männlichen Patienten entsprechen."""),
        dcc.Markdown("""Die Wichtigkeiten der Charakteristiken des Modells sind wie folgt:"""),
    ]


def get_model_desc_infection(auc, pop, pos):
    return [
        html.H2("Technische Details"),
        dcc.Markdown(
            """
             Unser Rechenmodell wurde mit Daten von {} Patienten (von denen {}% COVID-19 positiv waren), \
             die Kliniken in der Italienischen Stadt Cremona besucht hatten, trainert.
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona ist mit mehreren tausend positiven Fällen eine der am stärksten betroffenen italienischen 
             Provinzen in der Lombardei.
             """.format(pop[0], str(int(float(pos[0]) * 100))),
        ),
        html.Hr(),
        html.Div(
            [
             "Das Rechenmodell basiert auf ",
             html.A("den XGBoost Klassifikator.", href="https://xgboost.readthedocs.io/"),
             html.Br(),
             "Die Fläche unter der Kurve (AUC) von Vorhersagungen außerhalb der Stichproben von {} \
             Patienten (von denen {}% infiziert wurden) ist ".format(pop[1], str(int(float(pos[1]) * 100))),
             html.Span(' {}'.format(auc), style={'color': '#800020', "fontWeight": "bold"}), ".", html.Br(),
             "Wenn Eingabewerte fehlen, shreibt der Rechner seine eigenen Werte zu und zeigt sie an."
            ]
        ),
        html.Br(),
        dcc.Markdown(
            """Wir nutzen [SHAP Graphen](https://github.com/slundberg/shap) \
             um unsere XGBoost Modelle zu interpretieren. Die SHAP Grafik unten fasst Charakteristiken nach \
             ihrer Wichtigkeit und Direktionalität zusammen. Die Charakteristiken werden nach abnehmender Wichtigkeit \
             sortiert, mit der wichtigsten Charakteristik oben. Für eine gegeben Charakteristik zeigt die \
             korrespondierende Grafik wie stark der Einfluß der Charakteristik auf das Endergebniss ist, mit rot \
             als größter Einfluss und blau als kleinster. Höhere SHAP Werte entsprechen erhöhten Wahrscheinlichkeiten \
             eines positiven Endergebnisses (z.B. Todeswahrscheinlichkeit oder Infektionswahrscheinlichkeit). \
             Daher, Charakteristiken mit dem Farbverlauf von blau zu rot (von links nach rechts) haben einen \
             erhöhten Risikowert wenn die Charakteristik steigt, sowie mit Alter. Charakteristiken die von rot \
             zu blau verlaufen, haben einen niedrigeren Risikowert wenn die Charakteristik steigt, sowie mit \
             Sauerstoffsättigung. Hinweis: Geschlecht wird als Binärwert enkodiert (0=Männlich, 1=Weiblich), \
             sodass "niedrigere" Geschlechtswerte männlichen Patienten entsprechen."""),
        dcc.Markdown("""Die Wichtigkeiten der Charakteristiken des Modells sind wie folgt:"""),
    ]


def get_feature_names():
    return {
        'ABG: Oxygen Saturation (SaO2)': 'Sauerstoffsättigung',
        'Alanine Aminotransferase (ALT)': 'Alanin-Aminotransferase',
        'Age': 'Alter',
        'Aspartate Aminotransferase (AST)': 'Aspartate Aminotransferase',
        'Blood Creatinine': 'Blutkreatinin',
        'Blood Sodium': 'Natrium im Blut',
        'Blood Urea Nitrogen (BUN)': 'Blutharnstoffstickstoff',
        'Body Temperature': 'Temperatur',
        'C-Reactive Protein (CRP)': 'C-Reaktives Protein',
        'CBC: Hemoglobin': 'Hämoglobin',
        'CBC: Leukocytes': 'Leukozyten',
        'CBC: Mean Corpuscular Volume (MCV)': 'Mittleres Korpuskularvolumen',
        'CBC: Platelets': 'Thrombozyten',
        'CBC: Red cell Distribution Width (RDW)': 'Verteilungsbreite der roten Blutkörperchen',
        'Cardiac Frequency': 'Puls',
        'Gender': 'Geschlecht',
        'Glycemia': 'Blutzucker',
        'Potassium Blood Level': 'Kalium',
        'Prothrombin Time (INR)': 'Prothrombin-Zeit',
        'Systolic Blood Pressure': 'Systolischer Blutdruck',
        'SaO2': 'Sauerstoffsättigung',
        'Blood Calcium': 'Kalzium',
        'ABG: PaO2': 'Partialdruck Sauerstoff',
        'ABG: pH': 'Arterieller Blutgas-pH',
        'Cholinesterase': 'Cholinesterase',
        'Respiratory Frequency': 'Atemfrequenz',
        'ABG: MetHb': 'Arterielle Blutgas-Methämoglobinämie',
        'Total Bilirubin': 'Gesamt-Bilirubin',
        'Comorbidities': 'Komorbiditäten',
        'Diabetes': 'Diabetes',
        'Chronic kidney disease': 'Chronisches Nierenleiden',
        'Cardiac dysrhythmias': 'Herzrhythmusstörungen',
        'Coronary atherosclerosis and other heart disease': 'Koronare Atherosklerose und andere Herzerkrankungen'
    }
