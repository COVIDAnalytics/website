import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import flask
from dash.dependencies import Input, Output, State, ClientsideFunction
from flask import session

from datetime import datetime as dt

from interactive import InteractiveGraph, build_graph, all_options
from homepage import Homepage
from insights import Graphs
from projections import ProjectState, build_state_projection, build_us_map, get_us_stat
from team import Team
from dataset import Dataset
from contact import Contact
from dataset_documentation import Dataset_documentation

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.title = "MIT_ORC_COVID19"
app.config.suppress_callback_exceptions = True
external_stylesheets=[dbc.themes.BOOTSTRAP]

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# redirects to different pages
@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/interactive-graph':
        return InteractiveGraph()
    # if pathname == '/insights':
    #     return Graphs()
    if pathname == '/projections':
        return ProjectState()
    if pathname == '/team':
        return Team()
    if pathname == '/contact':
        return Contact()
    if pathname == '/dataset':
        return Dataset()
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

if __name__ == '__main__':
    app.run_server(debug=True)
