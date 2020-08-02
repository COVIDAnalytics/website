import os
from datetime import datetime as dt
import pandas as pd
from dash.dependencies import Output, Input
import flask

from projections.visuals_funcs import build_us_map, get_stat, build_continent_map, build_state_projection
from projections.utils import get_world_map_text, get_state_abbr


def register_callbacks(app):
    df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates=['Day'])
    df_projections.loc[:, 'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
    today = pd.Timestamp('today')
    df_projections = df_projections.loc[df_projections['Day'] >= today]

    pop_info = pd.read_csv('data/predicted/WorldPopulationInformation.csv', sep=",")

    @app.server.route('/DELPHI_documentation_pdf', methods=['GET', 'POST'])
    def download_delphi_documentation():
        return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                         filename="DELPHI_Documentation.pdf")

    @app.server.route('/Policy_evaluation_documentation', methods=['GET', 'POST'])
    def download_policy_eval_documentation():
        return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                         filename="Policy_Eval_Documentation.pdf")

    # Reset country_dropdown when main location (scope) changes
    @app.callback(
        [Output('country_dropdown', 'options'),
         Output('country_dropdown', 'clearable'),
         Output('continent_dropdown', 'value'),
         Output('country_dropdown', 'value')],
        [Input('location_map_dropdown', 'value')])
    def set_countries_options(selected_continent):
        if selected_continent == 'World':
            df = df_projections[(df_projections.Continent != 'None') & (df_projections.Country != 'None')]
            return [[{'label': i, 'value': i} for i in df.Country.unique()], True, None, None]
        if selected_continent != 'US':
            df = df_projections[(df_projections.Continent == selected_continent) & (df_projections.Country != 'None')]
            return [[{'label': i, 'value': i} for i in df.Country.unique()], True, selected_continent, None]
        else:
            df = df_projections[(df_projections.Continent == "North America") & (df_projections.Country != 'None')]
            return [[{'label': i, 'value': i} for i in df.Country.unique()], False, "North America", "US"]

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
        return "And for location"

    @app.callback(
        [Output('province_dropdown', 'options'),
         Output('province_dropdown', 'value'),
         Output('province_dropdown', 'disabled'),
         Output('country_dropdown', 'className'),
         Output('province_dropdown', 'style'),
         Output('country_dropdown', 'style'),
         Output('continent_dropdown', 'style')],
        [Input('country_dropdown', 'value')])
    def set_province_options(selected_country):
        default_class = ["loc-sel-drop loc-sel-slash "]
        no_province_class = [default_class[0] + "no-sel-slash", {"display": "none"},
                             {"width": "60%"}, {"width": "40%"}]
        yes_province_class = [default_class[0], {"display": "table"}]
        yes_us_class = [{"width": "25%"}, {"width": "50%"}]
        no_us_class = [{"width": "37.5%"}, {"width": "37.5%"}]
        countries_with_provinces = ["US", "Canada", "Australia"]
        if selected_country is None or selected_country not in countries_with_provinces:
            return [[], None, True] + no_province_class
        else:
            df = df_projections[df_projections.Country == selected_country]
            us_class = yes_us_class if selected_country == "US" else no_us_class
            return tuple([[{'label': get_state_abbr()[i], 'value': i} for i in df.Province.unique()],
                          None, False] + yes_province_class + us_class)

    @app.callback(
        [Output('state_projection_graph', 'children'),
         Output('predicted_timeline', 'className')],
        [Input('province_dropdown', 'value'),
         Input('country_dropdown', 'value'),
         Input('location_map_dropdown', 'value'),
         Input('predicted_timeline', 'value')
         ])
    def update_projection(state, country, continent, val):
        state = 'None' if state is None else state
        country = 'None' if country is None else country

        # make dropdwon text smaller if more options are selectedj
        dropdown_classes = "flat-map-multi "
        if len(val) > 1:
            dropdown_classes += "flat-map-multi-small"

        return build_state_projection(df_projections, state, country, continent, val), dropdown_classes

    @app.callback(
        Output('map_projections', 'children'),
        [Input('us-map-date-picker-range', 'date'),
         Input('us_map_dropdown', 'value'),
         Input('location_map_dropdown', 'value'),
         Input('radio_botton', 'value')])
    def update_us_map(chosen_date, val, location, pop):
        if location == 'US':
            return build_us_map(df_projections, pop_info, chosen_date, val, pop)
        else:
            return build_continent_map(df_projections, pop_info, chosen_date, val, location, pop)

    @app.callback(
        [Output('us_tot_det', 'children'),
         Output('us_active', 'children'),
         Output('us_active_hosp', 'children'),
         Output('us_tot_death', 'children')],
        [Input('us-map-date-picker-range', 'date'),
         Input('location_map_dropdown', 'value')])
    def update_stats(chosen_date, scope):
        return [get_stat(df_projections, chosen_date, 'Total Detected', scope),
                get_stat(df_projections, chosen_date, 'Active', scope),
                get_stat(df_projections, chosen_date, 'Active Hospitalized', scope),
                get_stat(df_projections, chosen_date, 'Total Detected Deaths', scope)]

    @app.callback(
        Output('us-stats-title', 'children'),
        [Input('us-map-date-picker-range', 'date'),
         Input('location_map_dropdown', 'value')])
    def display_us_stats_title(d, location):
        if d is not None:
            d = dt.strptime(d, '%Y-%m-%d').date()
            return u'{} Predicted {} Counts'.format(d.strftime('%b %d,%Y'), location)
        return ''

    @app.callback(
        Output("projection-notes-card", "style"),
        [Input("projection-show-notes-btn", "n_clicks")])
    def toggle_notes(clicks):
        print(clicks)
        if clicks is not None and clicks % 2 == 1:
            return {"maxHeight": "2000px", "opacity": "1.0", "padding": "10px"}
        else:
            return {"maxHeight": "0px", "opacity": "0.0", "margin": "0px"}
