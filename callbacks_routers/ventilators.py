from datetime import datetime as dt
import os
import pandas as pd
import urllib

from dash.dependencies import Output, Input
import flask

from ventilators.transfers_funcs import build_transfers_map,build_transfers_timeline,generate_table
from ventilators.utils import get_no_model_visual, us_map, us_timeline

def register_callbacks(app):
    df_mod1_transfers = pd.read_csv('data/predicted_ventilator/transfers_table-ihme.csv', sep=",", parse_dates = ['Date'])
    df_mod1_transfers.loc[:,'Date'] = pd.to_datetime(df_mod1_transfers['Date'], format='y%m%d').dt.date
    df_mod2_transfers = pd.read_csv('data/predicted_ventilator/transfers_table-ode.csv', sep=",", parse_dates = ['Date'])
    df_mod2_transfers.loc[:,'Date'] = pd.to_datetime(df_mod2_transfers['Date'], format='y%m%d').dt.date

    df_mod1_projections = pd.read_csv('data/predicted_ventilator/state_supplies_table_baseline-ihme.csv', sep=",", parse_dates = ['Date'])
    df_mod1_projections.loc[:,'Date'] = pd.to_datetime(df_mod1_projections['Date'], format='y%m%d').dt.date
    df_mod2_projections = pd.read_csv('data/predicted_ventilator/state_supplies_table_baseline-ode.csv', sep=",", parse_dates = ['Date'])
    df_mod2_projections.loc[:,'Date'] = pd.to_datetime(df_mod2_projections['Date'], format='y%m%d').dt.date

    @app.callback(
        Output('us_map_projections_vent', 'children'),
        [Input('base-model-dropdown', 'value'),
         Input('us-map-date-picker-range-vent', 'date'),
         Input('us_map_dropdown-vent', 'value')])
    def update_shortage_map(chosen_model,chosen_date,val):
        if chosen_model == "Washington IHME":
            df_map = df_mod1_projections
        else:
            df_map = df_mod2_projections
        no_model_visual = get_no_model_visual()
        return us_map(df_map,chosen_date,val,no_model_visual)

    @app.callback(
        Output('us_ventilator_graph', 'children'),
        [Input('base-model-dropdown', 'value')])
    def update_shortage_timeline(chosen_model):
        if chosen_model == "Washington IHME":
            df_projections_vent_us = df_mod1_projections
        else:
            df_projections_vent_us = df_mod2_projections
        df_projections_vent_us = df_projections_vent_us.loc[df_projections_vent_us.State == 'US']
        return us_timeline(df_projections_vent_us, "US Ventilator Supply, Demand, & Shortage", False)

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
        if chosen_model == "Washington IHME":
            df_opt_pre = df_mod1_projections
            df_opt_post = pd.read_csv('data/predicted_ventilator/state_supplies_table-ihme.csv', sep=",", parse_dates = ['Date'])
        else:
            df_opt_pre = df_mod2_projections
            df_opt_post = pd.read_csv('data/predicted_ventilator/state_supplies_table-ode.csv', sep=",", parse_dates = ['Date'])
        return build_transfers_timeline(df_opt_pre,df_opt_post,p1,p2,p3)

    @app.callback(
        Output('transfer-state-dropdown', 'options'),
        [Input('base-model-dropdown', 'value'),
        Input('date-transfer-dropdown', 'date'),
        Input('transfer-to-from-dropdown', 'value'),
        Input('p1-transfer-dropdown', 'value'),
        Input('p2-transfer-dropdown', 'value'),
        Input('p3-transfer-dropdown', 'value')])
    def set_transfer_state_options(chosen_model,chosen_date,to_or_from,p1,p2,p3):
        if chosen_model == "Washington IHME":
            df_trans = df_mod1_transfers
        else:
            df_trans = df_mod2_transfers
        if isinstance(chosen_date, str):
            chosen_date = dt.strptime(chosen_date, '%Y-%m-%d').date()
        df_trans = df_trans.loc[df_trans['Date']==chosen_date]
        df_trans = df_trans.loc[df_trans.Param1==float(p1)]
        df_trans = df_trans.loc[df_trans.Param2==float(p2)]
        df_trans = df_trans.loc[df_trans.Param3==float(p3)]
        if to_or_from == "to":
            return [{'label': x, 'value': x} for x in sorted(df_trans.State_To.unique())]
        else:
            return [{'label': x, 'value': x} for x in sorted(df_trans.State_From.unique())]

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
        if chosen_model == "Washington IHME":
            df_trans = df_mod1_transfers
        else:
            df_trans = df_mod2_transfers
        if isinstance(chosen_date, str):
            chosen_date = dt.strptime(chosen_date, '%Y-%m-%d').date()

        df_trans = df_trans.loc[
                                    (df_trans['Date']==chosen_date) & \
                                    (df_trans.Param1==float(p1)) & \
                                    (df_trans.Param2==float(p2)) & \
                                    (df_trans.Param3==float(p3))
                                ]
        if state is None:
            return generate_table(df_trans)
        return generate_table(df_trans,to_or_from,state)

    @app.callback(
        Output('download-link-demand', 'href'),
        [Input('base-model-dropdown', 'value')])
    def update_download_link_demand(chosen_model):
        if chosen_model == "Washington IHME":
            df_shortage = pd.read_csv('data/predicted_ventilator/state_supplies_table-ihme.csv', sep=",", parse_dates = ['Date'])
        else:
            df_shortage = pd.read_csv('data/predicted_ventilator/state_supplies_table-ode.csv', sep=",", parse_dates = ['Date'])
        df_shortage = df_shortage.to_csv(index=False, encoding='utf-8')
        return "data:text/csv;charset=utf-8," + urllib.parse.quote(df_shortage)

    @app.callback(
        Output('download-link-tranfers', 'href'),
        [Input('base-model-dropdown', 'value')])
    def update_download_link_transfers(chosen_model):
        if chosen_model == "Washington IHME":
            transfers_csv_string = df_mod1_transfers.to_csv(index=False, encoding='utf-8')
        else:
            transfers_csv_string = df_mod2_transfers.to_csv(index=False, encoding='utf-8')
        return "data:text/csv;charset=utf-8," + urllib.parse.quote(transfers_csv_string)

    @app.server.route('/ventilator_documentation_pdf', methods=['GET', 'POST'])
    def download_ventilator_documentation():
        return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                         filename="Ventilator_Documentation.pdf")
