from dash.dependencies import Input, Output

from interactive_graphs.interactive import InteractiveGraph, build_graph
from assets.mappings import data_cols,all_options

def register_callbacks(app):
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
