from dash.dependencies import Input, Output

from interactive_graphs.interactive import InteractiveGraph, build_graph

def register_callbacks(app):

    all_options = {
        'Comorbidities': [
            "Hypertension",
            "Diabetes",
            "Cardiovascular Disease (incl. CAD)",
            "Chronic obstructive lung (COPD)",
            "Cerebrovascular Disease",
            "Renal Disease",
        ],
        'Symptoms': [
            "Fever (temperature ≥37·3°C)",
            "Cough",
            "Fatigue",
            "Diarrhoea",
            "Shortness of Breath (dyspnoea)",
            "Nausea or Vomiting",
            "Loss of Appetite/Anorexia",
            "ARDS",
        ],
        'Treatment': [
            "Antiviral (Any)",
            "Uses Kaletra (lopinavir–ritonavir)",
            "Uses Arbidol (umifenovir)",
            "Corticosteroid (including Glucocorticoid, Methylprednisolone)",
            "Invasive mechanical ventilation",
        ],
        'Lab Test Results':[
            "White Blood Cell Count (10^9/L) - Median",
            "Lymphocyte Count (10^9/L) - Median",
            "Platelet Count (10^9/L) - Median",
            "C-Reactive Protein (mg/L)",
            "Hemoglobin (g/L) - Median",
            "Total Bilirubin (umol/L) - Median",
            "D-Dimer (mg/L)",
            "Albumin (g/L)"
        ],
    }

    @app.callback(
        Output('interactive_graph', 'children'),
        [Input('y_axis_dropdown', 'value'),
        Input('x_axis_dropdown', 'value'),
        Input('survivors', 'value'),]
    )
    def update_graph(y,x,survivor_vals):
        return build_graph(y,x,survivor_vals)

    @app.callback(
        Output('y_axis_dropdown', 'options'),
        [Input('categories_dropdown', 'value')])
    def set_y_options(selected_category):
        return [{'label': i, 'value': i} for i in all_options[selected_category]]

    @app.callback(
        Output('y_axis_dropdown', 'value'),
        [Input('categories_dropdown', 'options')])
    def set_y_value(available_options):
        return available_options[0]['value']

    @app.callback(
        Output('display-selected-values', 'children'),
        [Input('categories_dropdown', 'value')])
    def set_display_children(selected_category):
        mapping = {"Comorbidities": "Comorbidity", "Treatment": "Treatment", "Symptoms": "Symptom", "Lab Test Results":"Lab Test Result"}
        return u'Select the {} (Vertical Axis)'.format(mapping[selected_category])
