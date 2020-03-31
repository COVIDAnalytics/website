import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from interactive import App,build_graph,all_options
from homepage import Homepage
from insights import Graphs
from dash.dependencies import Input, Output, State, ClientsideFunction
from datetime import datetime as dt


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.title = "MIT_ORC_COVID19"
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/interactive-graph':
        return App()
    if pathname == '/insights':
        return Graphs()
    else:
        return Homepage()

@app.callback(
    Output('interactive_graph', 'children'),
    [Input('y_axis_dropdown', 'value'),
    Input('x_axis_dropdown', 'value'),
    Input('survivors', 'value'),]
)
def update_graph(y,x,survivor_vals):
    graph = build_graph(y,x,survivor_vals)
    return graph

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


if __name__ == '__main__':
    app.run_server(debug=True)
