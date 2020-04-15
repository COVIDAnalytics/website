import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import flask
import os

from datetime import datetime as dt

from interactive_graphs.interactive import InteractiveGraph, build_graph
from homepage import Homepage
from projections.projections import ProjectState, build_state_projection, build_us_map, get_us_stat
from about_us.team import Team
from dataset.dataset import Dataset
from about_us.contact import Contact
from dataset.dataset_documentation import Dataset_documentation
from projections.projections_documentation import Projections_documentation
from ventilators.allocations import VentilatorAllocations
from ventilators.shortage_funcs import build_shortage_map,build_shortage_timeline
from ventilators.transfers_funcs import build_transfers_map,build_transfers_timeline,build_transfer_options,generate_table
from ventilators.utils import build_download_link_demand, build_download_link_transfers
from risk_calculator.calculator import RickCalc, valid_input, predict_risk,build_feature_importance_graph
from risk_calculator.features import features
from assets.mappings import data_cols,all_options

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
    if pathname == '/calculator':
        return RickCalc()
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
@app.callback(
    Output('state_projection_graph', 'children'),
    [Input('state_dropdown', 'value'),
     Input('predicted_timeline', 'value')]
)
def update_projection(state,val):
    return build_state_projection(state,val)

@app.callback(
    Output('us_map_projections', 'children'),
    [Input('us-map-date-picker-range', 'date'),
     Input('us_map_dropdown', 'value')])
def update_us_map(chosen_date,val):
    return build_us_map(chosen_date,val)

@app.callback(
    Output('us_tot_det', 'children'),
    [Input('us-map-date-picker-range', 'date')])
def update_us_tot_det(chosen_date):
    return get_us_stat(chosen_date,'Total Detected')

@app.callback(
    Output('us_active', 'children'),
    [Input('us-map-date-picker-range', 'date')])
def update_us_tot_det(chosen_date):
    return get_us_stat(chosen_date,'Active')

@app.callback(
    Output('us_active_hosp', 'children'),
    [Input('us-map-date-picker-range', 'date')])
def update_us_tot_det(chosen_date):
    return get_us_stat(chosen_date,'Active Hospitalized')

@app.callback(
    Output('us_tot_death', 'children'),
    [Input('us-map-date-picker-range', 'date')])
def update_us_tot_det(chosen_date):
    return get_us_stat(chosen_date,'Total Detected Deaths')

@app.callback(
    Output('us-stats-title', 'children'),
    [Input('us-map-date-picker-range', 'date')])
def display_US_stats_title(d):
    d = dt.strptime(d, '%Y-%m-%d').date()
    return u'{} Predicted US Counts'.format(d.strftime('%b %d,%Y'))

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
    return flask.send_from_directory(directory=os.path.join(app.server.root_path, "assets"),
                                     filename="Ventilator_Documentation.pdf")


#callback for risk calculator
def get_type_inputs(amount,name):
    inputs = [None]*amount
    for k in range(amount):
        inputs[k] = State('calc-{}-{}'.format(name,k), 'value')
    return inputs

def get_feature_inputs():
    inputs = get_type_inputs(len(features['numeric']),'numeric')
    inputs += get_type_inputs(len(features['categorical']),'categorical')
    inputs += get_type_inputs(len(features['checkboxes']),'checkboxes')
    inputs += get_type_inputs(len(features['multidrop']),'multidrop')
    return inputs

@app.callback(
    [Output('score-calculator-card-body', 'children'),
    Output('calc-input-error', 'displayed'),
    Output('calc-input-error', 'message')],
    [Input('submit-features-calc', 'n_clicks')],
    get_feature_inputs()
)
def update_projection(*argv):
    default = html.H4("The mortality risk score is:",className="score-calculator-card-content"),
    #if submit button was clicked
    if argv[0] > 0:
        x = argv[1:]
        valid, err = valid_input(x)
        if valid:
            return predict_risk(x),False,''
        else:
            return default,True,err
    #user has not clicked submit
    return default,False,''

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
