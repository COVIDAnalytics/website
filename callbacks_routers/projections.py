import os
from datetime import datetime as dt

from dash.dependencies import Output, Input
import flask

from projections.visuals_funcs import build_us_map, get_stat, build_continent_map, build_state_projection
from projections.utils import get_df_projections, get_world_map_text

def register_callbacks(app):
    @app.server.route('/DELPHI_documentation_pdf', methods=['GET', 'POST'])
    def download_delphi_documentation():
        return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                         filename="DELPHI_Documentation.pdf")

    @app.server.route('/Policy_evaluation_documentation', methods=['GET', 'POST'])
    def download_policy_eval_documentation():
        return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                         filename="Policy_Eval_Documentation.pdf")

    #Reset country_dropdown when main location (scope) changes
    @app.callback(
        [Output('country_dropdown', 'options'),
         Output('country_dropdown', 'value'),
         Output('country_dropdown', 'disabled')],
        [Input('location_map_dropdown', 'value')])
    def set_countries_options(selected_continent):
        if selected_continent == 'World':
            df_projections = get_df_projections()
            df = df_projections[(df_projections.Continent != 'None') & (df_projections.Country != 'None')]
            return [[{'label': i, 'value': i} for i in df.Country.unique()], None, False]
        if selected_continent != 'US':
            df_projections = get_df_projections()
            df = df_projections[(df_projections.Continent == selected_continent) & (df_projections.Country != 'None')]
            return [[{'label': i, 'value': i} for i in df.Country.unique()], None, False]
        else:
            return [[{'label': 'US', 'value': 'US'}], 'US', True]

    @app.callback(
        Output('grey-countries-text', 'children'),
        [Input('location_map_dropdown', 'value')])
    def set_missing_country_text(selected_continent):
        if selected_continent is None or selected_continent == "US":
            return ''
        else:
            return get_world_map_text()

    @app.callback(
        Output('province-card-title', 'children'),
        [Input('location_map_dropdown', 'value')])
    def set_province_card_title(selected_continent):
        return "For which location in {}?".format(selected_continent)

    @app.callback(
        [Output('province_dropdown', 'options'),
         Output('province_dropdown', 'value'),
         Output('province_dropdown', 'disabled')],
        [Input('country_dropdown', 'value')])
    def set_province_options(selected_country):
        countries_with_provinces = ["US","Canada","Australia"]
        if selected_country is None or selected_country not in countries_with_provinces:
            return [[], None, True]
        else:
            df = get_df_projections()
            df = df[df.Country == selected_country]
            return [[{'label': i, 'value': i} for i in df.Province.unique()], None, False]

    @app.callback(
        Output('state_projection_graph', 'children'),
        [Input('province_dropdown', 'value'),
         Input('country_dropdown', 'value'),
         Input('location_map_dropdown', 'value'),
         Input('predicted_timeline', 'value')
         ])
    def update_projection(state, country, continent, val):
        state = 'None' if state == None else state
        country = 'None' if country == None else country
        return build_state_projection(state, country, continent, val)

    @app.callback(
        Output('map_projections', 'children'),
        [Input('us-map-date-picker-range', 'date'),
         Input('us_map_dropdown', 'value'),
         Input('location_map_dropdown', 'value'),
         Input('radio_botton', 'value')])
    def update_us_map(chosen_date,val, location,pop):
        if location == 'US':
            return build_us_map(chosen_date,val,pop)
        else:
            return build_continent_map(chosen_date,val, location,pop)

    @app.callback(
        [Output('us_tot_det', 'children'),
         Output('us_active', 'children'),
         Output('us_active_hosp', 'children'),
         Output('us_tot_death', 'children')],
        [Input('us-map-date-picker-range', 'date'),
         Input('location_map_dropdown', 'value')])
    def update_stats(chosen_date, scope):
        return [get_stat(chosen_date,'Total Detected', scope),
                get_stat(chosen_date,'Active', scope),
                get_stat(chosen_date,'Active Hospitalized', scope),
                get_stat(chosen_date,'Total Detected Deaths', scope)]

    @app.callback(
        Output('us-stats-title', 'children'),
        [Input('us-map-date-picker-range', 'date'),
         Input('location_map_dropdown', 'value')])
    def display_US_stats_title(d, location):
        if d is not None:
            d = dt.strptime(d, '%Y-%m-%d').date()
            return u'{} Predicted {} Counts'.format(d.strftime('%b %d,%Y'),location)
        return ''
