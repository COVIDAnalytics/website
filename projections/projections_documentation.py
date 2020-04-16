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
            	html.H2("Epidemiological Model Documentation"),
                html.P("""\
                        This page provides insights on a new epidemiological model developed by this team \
                        to provide estimates of the number of COVID-19 infections, hospitalizations, and \
                        deaths in all states of the United States. The model is based on the widely applied \
                        SEIR (Susceptible-Exposed-Infected-Recovered) modeling approach, which allocates every person to one of four states:
                       """),
                dcc.Markdown('''
                  1. Susceptible: The general population that has not been infected and is not immune.
                  2. Exposed: People who are currently infected, but are not contagious and lie within the incubation period.
                  3. Infected: People who are currently infected and are contagious.
                  4. Recovered: People who recovered and are immune.
                '''),
                html.P("""\
                        Using appropriate case-specific parameters, the SEIR modeling approach can then be applied \
                        to estimate the dynamics of a pandemic, as people move between these four states over time. \
                        This base model is then greatly expanded and adjusted for many factors important in the current \
                        COVID-19 pandemic, including under-detection, hospitalization, and societal counteracting measures. \
                        The parameter values are based on a meta-analysis of the data in the papers that the group curated.\
                        Important parameters are varied across different states:
                      """),
                # In developing the XYZ model, we have greatly expanded a basic SEIR model and made adjustments for many factors important
                dcc.Markdown('''
                  1. Effective contact rate: The effective contact rate measures the number of people that come into contact \
                  with an infected person per day. This fundamental quantity largely controls the spread of the virus, and \
                  would be greater in densely populated states (such as NY, CT) and smaller in sparsely populated ones (e.g. AZ, NV).
                  2. Societal/Governmental Response: This parameter measures, through a parametric nonlinear function, the impact \
                  of any governmental and societal responses on the spread of the virus over time. This includes such measures as \
                  government decrees regarding social distancing and sheltering-in-place, as well as increased hygiene-related \
                  awareness and reduced travel among the general population. This function is calibrated for every state to account \
                  for the differing responses in different states.
                '''),
				dcc.Markdown('''Detailed model specifications are available in the following \
                [technical report](/DELPHI_documentation_pdf). The full source code can be accessed on\
                [Github](https://github.com/COVIDAnalytics/epidemic-model).'''),
		 ],
	 ),
],
className="page-body"
)

def Projections_documentation():
    layout = html.Div([nav, body, footer],className="site")
    return layout
