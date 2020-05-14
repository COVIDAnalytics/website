import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import flask
import os
import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime as dt

from about_us.team import Team
from about_us.press import Press
from about_us.contact import Contact
from about_us.collaborators import Collaborators
from assets.mappings import data_cols,all_options
from dataset.dataset import Dataset
from dataset.dataset_documentation import Dataset_documentation
from homepage import Homepage
from interactive_graphs.interactive import InteractiveGraph
from projections.projections import ProjectState
from projections.projections_documentation import Projections_documentation
from policies.main import Policies, num_policies, build_policy_projections
from policies.cards import build_policy_cards
from risk_calculator.mortality.calculator import RiskCalc, valid_input_mort, predict_risk_mort, oxygen_in_mort, oxygen_mort_ind
from risk_calculator.infection.calculator import InfectionRiskCalc, valid_input_infec, predict_risk_infec, oxygen_in_infec, oxygen_infec_ind
from risk_calculator.features import build_feature_cards, build_feature_importance_graph, oxygen_options
from risk_calculator.utils import labs_features_mort, no_labs_features_mort, labs_features_infec, no_labs_features_infec
from risk_calculator.utils import languages, build_lab_ques_card, labs_ques
from risk_calculator.utils import no_labs_importance_mort, labs_importance_mort, no_labs_importance_infec, labs_importance_infec
from ventilators.allocations import VentilatorAllocations

import callbacks_routers.ventilators as ventilators
import callbacks_routers.insights as insights
import callbacks_routers.projections as projections

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

ventilators.register_callbacks(app)
insights.register_callbacks(app)
projections.register_callbacks(app)

@app.server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.server.root_path, 'static'),
                                     'favicon.ico', mimetype='image/x-icon')

# redirects to different pages
@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dataset':
        return Dataset()
    if pathname == '/dataset_documentation':
        return Dataset_documentation()
    if pathname == '/interactive-graph':
        return InteractiveGraph()
    if pathname == '/projections':
        return ProjectState()
    if pathname == '/projections_documentation':
        return Projections_documentation()
    if pathname == '/policies':
        return Policies()
    if pathname == '/ventilator_allocation':
        return VentilatorAllocations()
    if pathname == '/mortality_calculator':
        return RiskCalc()
    if pathname == '/infection_calculator':
        return InfectionRiskCalc()
    if pathname == '/team':
        return Team()
    if pathname == '/contact':
        return Contact()
    if pathname == '/press':
        return Press()
    if pathname == '/collaborators':
        return Collaborators()
    else:
        return Homepage()

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

#Callbacks for policies
options = \
    {
        'none': {
            'disabled':[{'label': '  No Restrictions', 'value': 'No_Measure', 'disabled': True}],
            'enabled':[{'label': '  No Restrictions', 'value': 'No_Measure', 'disabled': False}]
        },
        'lockdown': {
            'disabled':[{'label': '  Lockdown', 'value': 'Lockdown', 'disabled': True}],
            'enabled':[{'label': '  Lockdown', 'value': 'Lockdown', 'disabled': False}]
        },
        'mass': {
            'disabled':[{'label': '  Restrict Mass Gatherings', 'value': 'Mass_Gatherings', 'disabled': True}],
            'enabled':[{'label': '  Restrict Mass Gatherings', 'value': 'Mass_Gatherings', 'disabled': False}]
        },
        'schools': {
            'disabled':[{'label': '  Restrict Schools', 'value': 'Schools', 'disabled': True}],
            'enabled':[{'label': '  Restrict Schools', 'value': 'Schools', 'disabled': False}]
        },
        'others': {
            'disabled':[{'label': '  Restrict Non-Essential Businesses, Travel Restriction and Workplaces', 'value': 'Others', 'disabled': True}],
            'enabled':[{'label': '  Restrict Non-Essential Businesses, Travel Restriction and Workplaces', 'value': 'Others', 'disabled': False}]
        }
    }
for p in range(num_policies):
    @app.callback(
        [Output({'type': 'none', 'index': p}, "options"),
        Output({'type': 'lockdown', 'index': p}, "options"),
        Output({'type': 'mass', 'index': p}, "options"),
        Output({'type': 'schools', 'index': p}, "options"),
        Output({'type': 'others', 'index': p}, "options")],
        [Input({'type': 'none', 'index': p}, "value"),
        Input({'type': 'lockdown', 'index': p}, "value"),
        Input({'type': 'mass', 'index': p}, "value"),
        Input({'type': 'schools', 'index': p}, "value"),
        Input({'type': 'others', 'index': p}, "value"),]
    )
    def update_policy_options(no_measure,lockdown,mass,schools,others):
        if no_measure:
            return [options['none']['enabled'],options['lockdown']['disabled'],options['mass']['disabled'],options['schools']['disabled'],options['others']['disabled']]
        if lockdown:
            return [options['none']['disabled'],options['lockdown']['enabled'],options['mass']['disabled'],options['schools']['disabled'],options['others']['disabled']]
        if mass:
            return [options['none']['disabled'],options['lockdown']['disabled'],options['mass']['enabled'],options['schools']['enabled'],options['others']['enabled']]
        if others:
            return [options['none']['disabled'],options['lockdown']['disabled'],options['mass']['enabled'],options['schools']['disabled'],options['others']['enabled']]
        return [options['none']['enabled'],options['lockdown']['enabled'],options['mass']['enabled'],options['schools']['disabled'],options['others']['enabled']]

    @app.callback(
        Output('policy-week-text-{}'.format(p), 'children'),
        [Input({'type': 'timeline', 'index': p}, "value")]
    )
    def get_text_for_timeline(t):
        if t == 0:
            return "Policy change taking effect now."
        if t == 1:
            return "Policy change taking effect 1 week from now."
        if t == 2:
            return "Policy change taking effect 2 weeks from now."
        if t == 3:
            return "Policy change taking effect 4 weeks from now."
        return "Policy change taking effect 6 weeks from now."

@app.callback(
    [Output('policy_projection_graph', 'children'),
    Output('policy_deaths_projection_graph', 'children')],
    [Input('state_policies', "value"),
    Input({'type': 'none', 'index': ALL}, "value"),
    Input({'type': 'lockdown', 'index': ALL}, "value"),
    Input({'type': 'mass', 'index': ALL}, "value"),
    Input({'type': 'schools', 'index': ALL}, "value"),
    Input({'type': 'others', 'index': ALL}, "value"),
    Input({'type': 'none', 'index': ALL}, "options"),
    Input({'type': 'lockdown', 'index': ALL}, "options"),
    Input({'type': 'mass', 'index': ALL}, "options"),
    Input({'type': 'schools', 'index': ALL}, "options"),
    Input({'type': 'others', 'index': ALL}, "options"),
    Input({'type': 'timeline', 'index': ALL}, "value")]
)
def get_policy_projections(*argv):
    policy_options = 5
    input_policies = argv[1:policy_options+1]
    input_options = argv[policy_options+1:-1]
    times = argv[-1]
    policies = [[0,0,0,0,0] for i in range(num_policies)]
    for p in range(num_policies):
        for i in range(policy_options):
            if input_options[i][p]:
                if input_policies[i][p] and not input_options[i][p][0]["disabled"]:
                    policies[p][i] = 1
    return [build_policy_projections(argv[0],policies,times,"Total Detected"),
                build_policy_projections(argv[0],policies,times,"Total Detected Deaths")]

if __name__ == '__main__':
    app.run_server(debug=True)
