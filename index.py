import json
import urllib.parse
import sys

from flask import Flask
from flask_restful import Resource, Api

from api.rest_interface import MortalityCalcNoLabsEndpoint, MortalityCalcLabsEndpoint, InfectionCalcLabsEndpoint,\
    InfectionCalcNoLabsEndpoint

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import flask
import os

from about_us.team import Team
from about_us.press import Press
from about_us.contact import Contact
from about_us.collaborators import Collaborators
from dataset.dataset import Dataset
from dataset.dataset_documentation import Dataset_documentation
from homepage import Homepage
from interactive_graphs.interactive import InteractiveGraph
from projections.projections import ProjectState
from projections.projections_documentation import Projections_documentation
from policies.main import Policies
from risk_calculator.mortality.calculator import RiskCalc
from risk_calculator.infection.calculator import InfectionRiskCalc
from ventilators.allocations import VentilatorAllocations
from financial.main import FinancialReliefPlanning

import callbacks_routers.ventilators as ventilators
import callbacks_routers.insights as insights
import callbacks_routers.projections as projections
import callbacks_routers.risk_calculators_mortality as risk_calculators_mortality
import callbacks_routers.risk_calculators_infection as risk_calculators_infection
import callbacks_routers.policies as policies

external_stylesheets = [
    dbc.themes.UNITED,
    {
        'href': "https://fonts.googleapis.com/icon?family=Material+Icons",
        'rel': 'stylesheet',
        'crossorigin': 'anonymous'
    }
]
server = Flask('covidanalytics')
app = dash.Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
        server=server
    )

api = Api(server)
api.add_resource(MortalityCalcNoLabsEndpoint, "/api/mortality_calc_no_labs")
api.add_resource(MortalityCalcLabsEndpoint, "/api/mortality_calc_labs")
api.add_resource(InfectionCalcNoLabsEndpoint, "/api/infection_calc_no_labs")
api.add_resource(InfectionCalcLabsEndpoint, "/api/infection_calc_labs")

app.title = "COVIDAnalytics"
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
app.scripts.append_script({'external_url': 'https://covidanalytics.io/assets/gtag.js'})
app.scripts.append_script({'external_url': 'https://localhost:8085/assets/js/aos.js'})
app.scripts.append_script({'external_url': 'https://localhost:8085/assets/js/index.js'})

ventilators.register_callbacks(app)
insights.register_callbacks(app)
projections.register_callbacks(app)
risk_calculators_mortality.register_callbacks(app)
risk_calculators_infection.register_callbacks(app)
policies.register_callbacks(app)


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
    if pathname == '/financial_relief':
        return FinancialReliefPlanning()
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
    if len(sys.argv) == 1:
        app.run_server(debug=True)
    else: 
        app.run_server(debug=True, host=sys.argv[1])
