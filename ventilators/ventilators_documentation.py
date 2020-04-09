### Dash
import dash
import flask
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer

nav = Navbar()
footer = Footer()

body = dbc.Container([
	dbc.Row(
        [
			dbc.Col([
            	html.H2("Ventilator Allocation Documentation"),
                dcc.Markdown("Detailed model specifications are available in the following technical report."),
                html.P("""\
                        blah
                       """),
				 ])
		 ],
	 ),
],
className="page-body"
)

def Ventilator_documentation():
    layout = html.Div([nav, body, footer],className="site")
    return layout
