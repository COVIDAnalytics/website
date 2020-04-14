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
            	html.H2("Risk Calculator Model Documentation"),
                html.P("""\

                       """),
                dcc.Markdown('''

                '''),
                html.P("""\

                      """),
                # In developing the XYZ model, we have greatly expanded a basic SEIR model and made adjustments for many factors important
                dcc.Markdown('''
                  '''),
				dcc.Markdown('''
                  Additional documentation and the source code can be found here.
                '''),
				 ])
		 ],
	 ),
],
className="page-body"
)

def Risk_Calculator_documentation():
    layout = html.Div([nav, body, footer],className="site")
    return layout
