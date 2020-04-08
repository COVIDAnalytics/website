import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import flask

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
    mapping = {"Comorbidities": "Comorbidity", "Treatment": "Treatment", "Symptoms": "Symptom"}
    return u'Select the {} (Vertical Axis)'.format(mapping[selected_category])

#Callbacks for projections
@app.callback(
    Output('state_projection_graph', 'children'),
    [Input('state_dropdown', 'value'),]
)
def update_projection(state):
    return build_state_projection(state)

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
def update_us_vent_map(chosen_model,chosen_date,val):
    return build_us_vent_map(chosen_model,chosen_date,val)

@app.callback(
    Output('us_ventilator_graph', 'children'),
    [Input('base-model-dropdown', 'value'),
     Input('us_map_dropdown-vent', 'value')])
def update_us_vent_timeline(chosen_model,val):
    return build_us_vent_timeline(chosen_model,val)

@app.callback(
    Output('time_x_graph', 'children'),
    [Input('base-model-dropdown', 'value'),
     Input('us_map_dropdown-vent', 'value')])
def update_us_vent_peaks(chosen_model,val):
    return build_us_vent_peaks(chosen_model,val)

@app.callback(
    Output('us_map_transfers_vent', 'children'),
    [Input('base-model-dropdown_transfers', 'value'),
     Input('date-transfer-dropdown', 'date'),
     Input('val-transfer-dropdown', 'value'),
     Input('p1-transfer-dropdown', 'value'),
     Input('p2-transfer-dropdown', 'value'),
     Input('p3-transfer-dropdown', 'value')])
def update_us_transfers_map(chosen_model,chosen_date,val,p1,p2,p3):
    return build_us_transfers_map(chosen_model,chosen_date,val,p1,p2,p3)

@app.callback(
    Output('transfer-state-dropdown', 'options'),
    [Input('base-model-dropdown_transfers', 'value'),
    Input('transfer-to-from-dropdown', 'value')])
def set_transfer_state_options(chosen_model,to_or_from):
    return build_transfers(chosen_model,to_or_from)

@app.callback(
    Output('transfer_list', 'children'),
    [Input('base-model-dropdown_transfers', 'value'),
     Input('date-transfer-dropdown', 'date'),
     Input('transfer-to-from-dropdown', 'value'),
     Input('transfer-state-dropdown', 'value')])
def update_us_transfers(chosen_model,chosen_date,to_or_from,state):
    return build_us_transfers(chosen_model,chosen_date,to_or_from,state)

@app.callback(
    Output('download-link-demand', 'href'),
    [Input('base-model-dropdown_download', 'value')])
def update_download_link_demand(chosen_model):
    return build_download_link_demand(chosen_model)

@app.callback(
    Output('download-link-tranfers', 'href'),
    [Input('base-model-dropdown_download', 'value')])
def update_download_link_transfers(chosen_model):
    return build_download_link_transfers(chosen_model)



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
