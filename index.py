import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from interactive import App,build_graph
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
    [Input('country_pop_dropdown', 'value')]
)
def update_graph(city):
    graph = build_graph(city)
    return graph

@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

if __name__ == '__main__':
    app.run_server(debug=True)
