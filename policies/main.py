import json
import sklearn
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

nav = Navbar()
footer = Footer()

with open('assets/policies/US_Scenarios.json', 'rb') as file:
    projections = json.load(file)

states = list(projections.keys())

for k,v in projections.items():
    for key,val in v.items():
        if key == "Day":
            continue
        elif len(val)!=5:
            print(k,key)


body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Jumbotron(
                [
                    html.H2("Title"),
                    dcc.Markdown(
                         """text
                         """,
                    ),
                    html.Hr(),
                    dcc.Markdown(
                         """text
                         """,
                    )
                ],
                style={'paddingBottom':'0.5rem','paddingTop':'0.8rem'}
                )
            ]
            ),
        ],
        )
    ] + \
    get_labs_indicator('lab_values_indicator_infection') + \
    get_feature_cards('features-infection') + \
    get_submit_button('submit-features-calc-infection') + \
    get_results_card('score-calculator-card-body-infection','calc-input-error-infection') + \
    get_inputed_vals('imputed-text-infection') + \
    get_model_desc('infection-model-desc') + \
    get_feature_importance('feature-importance-bar-graph-infection'),
    className="page-body"
)

def Policies():
    layout = html.Div([nav, body, footer], className="site")
    return layout
