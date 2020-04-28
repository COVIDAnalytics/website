from textwrap import wrap
import plotly.graph_objects as go
import dash_core_components as dcc

from risk_calculator.mortality.calculator import model as mortality_model
from risk_calculator.infection.calculator import labs_model, no_labs_model

def convert_temp_units(x):
    return (x-32)/1.8


def build_feature_importance_graph(m="mortality",labs="No"):
    if m == "mortality":
        model = mortality_model
    else:
        model = no_labs_model if labs == "No" else labs_model
    feature_list = ['']*len(model.feature_importances_)
    i = 0
    for feat in features["numeric"]:
        feature_list[feat["index"]] = feat["name"]
        i+=1
    for feat in features["categorical"]:
        feature_list[feat["index"]] = feat["name"]
        i+=1
    for feat in features["checkboxes"]:
        for j,name in enumerate(feat["vals"]):
            feature_list[feat["index"][j]] = name
            i+=1
    for feat in features["multidrop"]:
        for j,name in enumerate(feat["vals"]):
            feature_list[feat["index"][j]] = name
            i+=1
    importances = list(model.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)[:10]
    x,y = zip(*feature_importances)
    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color="#800020"))])
    graph = dcc.Graph(
        id='feature-importance-graph',
        figure=fig,
    )

    fig.update_layout(
                height=450,
                title={
                    'text':'<br>'.join(wrap('<b> Feature Importance Graph </b>', width=30)) ,
                     'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_color='black',
                title_font_size=18,
                xaxis={'title': "Features",'linecolor': 'lightgrey'},
                yaxis={'title': "Importance",'linecolor': 'lightgrey'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )
    return graph
