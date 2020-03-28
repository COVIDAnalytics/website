import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("COVID-19"),
                     html.H2("Predictive Tools"),
                     html.P(
                         """\
                         MIT’s Operations Research Center provides open source interactive tools and dataset to predict patients outcome probabilities, including their potential Intensive Care Unit needs and expected length of stay in hospital.

                         We aim to rapidly develop, vet, and deliver tools for use by hospitals in the United States to combat the spread of COVID-19.

                         """
                           ),
                           dbc.Button("View details", color="secondary"),
                   ],
                  md=4,
               ),
              dbc.Col(
                 [
                     html.H2("We are a positive Team, Flattening the Curve"),
                     dcc.Graph(
                         figure={"data": [{"x": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "y": [1, 4, 9, 20, 50, 100, 220, 500, 550, 550, 550, 400, 330, 300, 250]}]}
                            ),
                        ]
                     ),
                ]
            )
       ],
className="mt-4",
)

def Homepage():
    layout = html.Div([
                    nav,
                    body
                    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()
app.title = "MIT_ORC_COVID19"
