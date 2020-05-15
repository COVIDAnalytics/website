from datetime import datetime as dt
import os

from dash.dependencies import Output, Input
import flask

from ventilators.shortage_funcs import build_shortage_map,build_shortage_timeline
from ventilators.transfers_funcs import build_transfers_map,build_transfers_timeline,build_transfer_options,generate_table
from ventilators.utils import build_download_link_demand, build_download_link_transfers

def register_callbacks(app):
    @app.callback(
        Output('us_map_projections_vent', 'children'),
        [Input('base-model-dropdown', 'value'),
         Input('us-map-date-picker-range-vent', 'date'),
         Input('us_map_dropdown-vent', 'value')])
    def update_shortage_map(chosen_model,chosen_date,val):
        return build_shortage_map(chosen_model,chosen_date,val)

    @app.callback(
        Output('us_ventilator_graph', 'children'),
        [Input('base-model-dropdown', 'value')])
    def update_shortage_timeline(chosen_model):
        return build_shortage_timeline(chosen_model)

    @app.callback(
        Output('us_map_transfers_vent', 'children'),
        [Input('base-model-dropdown', 'value'),
         Input('date-transfer-dropdown', 'date'),
         Input('p1-transfer-dropdown', 'value'),
         Input('p2-transfer-dropdown', 'value'),
         Input('p3-transfer-dropdown', 'value')])
    def update_us_transfers_map(chosen_model,chosen_date,p1,p2,p3):
        return build_transfers_map(chosen_model,chosen_date,p1,p2,p3)

    @app.callback(
        Output('us_transfers_graph', 'children'),
        [Input('base-model-dropdown', 'value'),
         Input('p1-transfer-dropdown', 'value'),
         Input('p2-transfer-dropdown', 'value'),
         Input('p3-transfer-dropdown', 'value')])
    def update_us_vent_timeline(chosen_model,p1,p2,p3):
        return build_transfers_timeline(chosen_model,p1,p2,p3)

    @app.callback(
        Output('transfer-state-dropdown', 'options'),
        [Input('base-model-dropdown', 'value'),
        Input('date-transfer-dropdown', 'date'),
        Input('transfer-to-from-dropdown', 'value'),
        Input('p1-transfer-dropdown', 'value'),
        Input('p2-transfer-dropdown', 'value'),
        Input('p3-transfer-dropdown', 'value')])
    def set_transfer_state_options(chosen_model,chosen_date,to_or_from,p1,p2,p3):
        return build_transfer_options(chosen_model,chosen_date,to_or_from,p1,p2,p3)

    @app.callback(
        Output('table-text', 'children'),
        [Input('date-transfer-dropdown', 'date')])
    def set_font_for_table(chosen_date):
        return u'The table below lists all interstate transfers scheduled on \
            {} (empty if none are scheduled). Try changing the date above to see which \
            transfers are recommended on \
            other days!'.format(dt.strptime(chosen_date, '%Y-%m-%d').date().strftime('%b %d, %Y'))

        if to_or_from == "to":
            return u'The following presents which states send how many ventilators to {}'.format(state)
        else:
            return u'The following presents which states receive how many ventilators from {}'.format(state)

    @app.callback(
        Output('table-container', 'children'),
        [Input('base-model-dropdown', 'value'),
         Input('date-transfer-dropdown', 'date'),
         Input('transfer-to-from-dropdown', 'value'),
         Input('transfer-state-dropdown', 'value'),
         Input('p1-transfer-dropdown', 'value'),
         Input('p2-transfer-dropdown', 'value'),
         Input('p3-transfer-dropdown', 'value')])
    def display_table(chosen_model,chosen_date,to_or_from,state,p1,p2,p3):
        if state is None:
            return generate_table(chosen_model,chosen_date,p1,p2,p3)
        return generate_table(chosen_model,chosen_date,p1,p2,p3,to_or_from,state)

    @app.callback(
        Output('download-link-demand', 'href'),
        [Input('base-model-dropdown', 'value')])
    def update_download_link_demand(chosen_model):
        return build_download_link_demand(chosen_model)

    @app.callback(
        Output('download-link-tranfers', 'href'),
        [Input('base-model-dropdown', 'value')])
    def update_download_link_transfers(chosen_model):
        return build_download_link_transfers(chosen_model)


    @app.server.route('/ventilator_documentation_pdf', methods=['GET', 'POST'])
    def download_ventilator_documentation():
        return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                         filename="Ventilator_Documentation.pdf")
