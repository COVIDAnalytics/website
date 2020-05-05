import json
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from policies.cards import get_state_num_policy_card

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
    get_state_num_policy_card(states),
    className="page-body"
)

def Policies():
    layout = html.Div([nav, body, footer], className="site")
    return layout
