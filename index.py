import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import flask
import os

from datetime import datetime as dt

from about_us.team import Team
from about_us.press import Press
from about_us.contact import Contact
from assets.mappings import data_cols,all_options
from dataset.dataset import Dataset
from dataset.dataset_documentation import Dataset_documentation
from homepage import Homepage
from interactive_graphs.interactive import InteractiveGraph, build_graph
from projections.projections import ProjectState
from projections.visuals_funcs import build_us_map, get_stat, build_continent_map, build_state_projection
from projections.utils import df_projections, countries_with_provinces, world_map_text
from projections.projections_documentation import Projections_documentation
from risk_calculator.mortality.calculator import RiskCalc, valid_input_mort, predict_risk_mort, labs_features_mort, no_labs_features_mort
from risk_calculator.infection.calculator import InfectionRiskCalc, valid_input_infec, predict_risk_infec, labs_features_infec, no_labs_features_infec
from risk_calculator.features import build_feature_cards, build_feature_importance_graph
from ventilators.allocations import VentilatorAllocations
from ventilators.shortage_funcs import build_shortage_map,build_shortage_timeline
from ventilators.transfers_funcs import build_transfers_map,build_transfers_timeline,build_transfer_options,generate_table
from ventilators.utils import build_download_link_demand, build_download_link_transfers

app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.UNITED],
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ]
        )
server = app.server
app.title = "COVIDAnalytics"
app.config.suppress_callback_exceptions = True
external_stylesheets=[dbc.themes.BOOTSTRAP]

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])
app.scripts.append_script({'external_url':'https://covidanalytics.io/assets/gtag.js'})

@app.server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.server.root_path, 'static'),
                                     'favicon.ico', mimetype='image/x-icon')

# redirects to different pages
@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/interactive-graph':
        return InteractiveGraph()
    if pathname == '/projections':
        return ProjectState()
    if pathname == '/team':
        return Team()
    if pathname == '/contact':
        return Contact()
    if pathname == '/dataset':
        return Dataset()
    if pathname == '/projections_documentation':
        return Projections_documentation()
    if pathname == '/dataset_documentation':
        return Dataset_documentation()
    if pathname == '/ventilator_allocation':
        return VentilatorAllocations()
    if pathname == '/mortality_calculator':
        return RiskCalc()
    if pathname == '/infection_calculator':
        return InfectionRiskCalc()
    if pathname == '/press':
        return Press()
    else:
        return Homepage()

#Callbacks for interactive
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

#Callbacks for projections

@app.server.route('/DELPHI_documentation_pdf', methods=['GET', 'POST'])
def download_delphi_documentation():
    return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets/documentations"),
                                     filename="DELPHI_Documentation.pdf")

#Reset country_dropdown when main location (scope) changes
@app.callback(
    [Output('country_dropdown', 'options'),
     Output('country_dropdown', 'value'),
     Output('country_dropdown', 'disabled')],
    [Input('location_map_dropdown', 'value')])
def set_countries_options(selected_continent):
    if selected_continent == 'World':
        df = df_projections[(df_projections.Continent != 'None') & (df_projections.Country != 'None')]
        return [[{'label': i, 'value': i} for i in df.Country.unique()], None, False]
    if selected_continent != 'US':
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
        return world_map_text

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
    if selected_country is None or selected_country not in countries_with_provinces:
        return [[], None, True]
    else:
        df = df_projections[df_projections.Country == selected_country]
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

#

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
    d = dt.strptime(d, '%Y-%m-%d').date()
    return u'{} Predicted {} Counts'.format(d.strftime('%b %d,%Y'),location)

#Callbacks for ventilators
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


#callback for risk calculators
@app.callback(
    Output('infection-model-desc', 'children'),
    [Input('lab_values_indicator_infection', 'value')])
def get_infection_model_desc(labs):
    return 'this is a dynamic description that depends on the model chosen above'

@app.callback(
    Output('mortality-model-desc', 'children'),
    [Input('lab_values_indicator', 'value')])
def get_mortality_model_desc(labs):
    return 'this is a dynamic description that depends on the model chosen above'

@app.callback(
    Output('feature-importance-bar-graph-infection', 'children'),
    [Input('lab_values_indicator_infection', 'value')])
def get_infection_model_feat_importance(labs):
    return build_feature_importance_graph(False,labs)

@app.callback(
    Output('feature-importance-bar-graph', 'children'),
    [Input('lab_values_indicator', 'value')])
def get_mortality_model_feat_importance(labs):
    return build_feature_importance_graph(True,labs)

@app.callback(
    Output('features-infection', 'children'),
    [Input('lab_values_indicator_infection', 'value')])
def get_infection_model_feat_cards(labs):
    return build_feature_cards(False,labs)

@app.callback(
    Output('features-mortality', 'children'),
    [Input('lab_values_indicator', 'value')])
def get_mortality_model_feat_cards(labs):
    return build_feature_cards(True,labs)

def get_type_inputs(amount,name):
    inputs = [None]*amount
    for k in range(amount):
        inputs[k] = State('calc-{}-{}'.format(name,k), 'value')
    return inputs

def get_feature_inputs(mortality=True,labs=False):
    if mortality:
        features = labs_features_mort if labs else no_labs_features_mort
    else:
        features = labs_features_infec if labs else no_labs_features_infec
    inputs = get_type_inputs(len(features['numeric']),'numeric')
    inputs += get_type_inputs(len(features['categorical']),'categorical')
    inputs += get_type_inputs(len(features['checkboxes']),'checkboxes')
    inputs += get_type_inputs(len(features['multidrop']),'multidrop')
    inputs += [State('calc-temp-f-c', 'value')]
    return inputs

@app.callback(
    [Output('score-calculator-card-body', 'children'),
    Output('calc-input-error', 'displayed'),
    Output('calc-input-error', 'message'),
    Output('imputed-text-mortality', 'children')],
    [Input('submit-features-calc', 'n_clicks'),
    Input('lab_values_indicator', 'value')],
    [State({'type': 'mortality', 'index': ALL}, 'value')]
)
def calc_risk_score(*argv):
    default = html.H4("The mortality risk score is:",className="score-calculator-card-content-infection"),
    submit = argv[0]
    labs = argv[1]
    #if submit button was clicked
    if submit > 0:
        x = argv[2:]
        valid, err, x = valid_input_mort(labs,x)
        if valid:
            score, imputed = predict_risk_mort(labs,x)
            return score,False,'',imputed
        else:
            return default,True,err,''
    #user has not clicked submit
    return default,False,'',''

@app.callback(
    [Output('score-calculator-card-body-infection', 'children'),
    Output('calc-input-error-infection', 'displayed'),
    Output('calc-input-error-infection', 'message'),
    Output('imputed-text-infection', 'children')],
    [Input('submit-features-calc-infection', 'n_clicks'),
    Input('lab_values_indicator_infection', 'value')],
    [State({'type': 'infection', 'index': ALL}, 'value')]
)
def calc_risk_score_infection(*argv):
    default = html.H4("The infection risk score is:",className="score-calculator-card-content-infection"),
    submit = argv[0]
    labs = argv[1]
    #if submit button was clicked
    if submit > 0:
        x = argv[2:]
        valid, err, x, missing = valid_input_infec(labs,x)
        if valid:
            score, imputed = predict_risk_infec(labs,x,missing)
            return score,False,'',imputed
        else:
            return default,True,err,''
    #user has not clicked submit
    return default,False,'',''

#Callbacks for navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
