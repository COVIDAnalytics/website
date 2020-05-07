import json
import plotly.graph_objects as go
import plotly.express as px
from textwrap import wrap
import math

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from policies.cards import get_state_num_policy_card, get_policy_cards, colors
from policies.graphs import get_projections, map_time, map_policy, no_policy_chosen, name_to_json, get_start

nav = Navbar()
footer = Footer()

with open('assets/policies/US_Scenarios.json', 'rb') as file:
    projections = json.load(file)

states = list(projections.keys())
num_policies = 3

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Jumbotron(
                [
                    html.H2("Predictions of infections and deaths under a variety of policies"),
                    dcc.Markdown(
                         """Using an extension of our [DELPHI model](/projections), we make predictions \
                         until September 2020 for infections and deaths for all states of the US. \
                         By selecting the state,  the collection of policies imposed and their timing, \
                         the user can compare up to 3 policies simultaneously.
                         """,
                    ),
                    html.Hr(),
                    dcc.Markdown(
                         """The methodology of the model is explained [here](/Policy_evaluation_documentation). \
                         We are currently developing an extension of the model for the world.
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
    get_state_num_policy_card(states) + \
    get_policy_cards(num_policies) + \
    get_projections(),
    className="page-body"
)

def Policies():
    layout = html.Div([nav, body, footer], className="site")
    return layout


def build_policy_projections(state, policies, times, value):
    if no_policy_chosen(policies):
        return

    fig = go.Figure()

    data = projections[state]
    x = data["Day"]
    max_y = 0
    for p,policy in enumerate(policies):
        if sum(policy) > 0:
            name = map_policy(policy)
            code = name_to_json[name]
            t = map_time[times[p]]
            y = data[code][t][value]
            fig.add_trace(go.Scatter(
                name='<br>'.join(wrap(name + "," + str(t), width=60)),
                showlegend=True,
                x=x,
                y=y,
                mode="lines",
                marker=dict(color=colors[p]),
                line=dict(color=colors[p],width=4)
            ))
            temp = max(data[code][t][value])
            if temp > max_y:
                max_y = int(math.ceil(temp / 100000.0)) * 100000

    for p,policy in enumerate(policies):
        if sum(policy) > 0:
            y = list(range(0,max_y+1,100000))
            x_vertical = [get_start(times[p])] * len(y)
            fig.add_trace(go.Scatter(
                showlegend=False,
                x=x_vertical,
                y=y,
                line=dict(color=colors[p], width=1, dash='dash'),
                marker=dict(color=colors[p], size=1)
            ))
    i= 0
    y = []
    while not math.isnan(data[value + " True"][i]):
        y.append(data[value + " True"][i])
        i+=1
    x = x[:len(y)]

    fig.add_trace(go.Scatter(
        name='<br>'.join(wrap("Truth", width=60)),
        showlegend=True,
        x=x,
        y=y,
        mode="lines",
        marker=dict(color='grey'),
        line=dict(color='grey',width=4)
    ))

    title = '<br>'.join(wrap('<b> {} for {} </b>'.format(value,state), width=35))
    fig.update_layout(
                height=550,
                title={
                    'text': title,
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Date",'linecolor': 'lightgrey'},
                yaxis={'title': "Count",'linecolor': 'lightgrey'},
                legend_title='<b> Values Predicted </b>',
                margin={'l': 40, 'b': 80, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend={
                        "orientation": "v",
                        "xanchor": "center",
                        "y": -0.6,
                        "x": 0.5
                        },
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )

    graph = dcc.Graph(
        id='{}-projection-graph'.format(value),
        figure=fig
    )
    return graph
