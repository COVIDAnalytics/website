### Data
import pandas as pd
import pickle
from datetime import datetime as dt
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar

df = pd.read_csv('data/0327.csv')

nav = Navbar()

categories = ["Comorbidities","Symptoms","Treatment"]
all_options = {
    'Comorbidities': ["Current Smoker"
                          ,"Any Comorbidity"
                          ,"Hypertension"
                          ,"Diabetes"
                          ,"Coronary.heart.disease"
                          ,"Chronic.obstructive.lung"
                          ,"Cancer..Any."
                          ,"Chronic.kidney.renal.disease"
                          ,"Other"
                     ],
    'Symptoms': ["Fever,temperature > 37.3 C"
                 ,"Average temperature (C)"
                 ,"Cough"
                 ,"Shortness of Breath (Dyspnoea)"
                 ,"Headache"
                 ,"Sputum"
                 ,"Muscle.Pain (Myalgia)"
                 ,"Fatigue"
                 ,"Diarrhoea"
                 ,"Nausea/Vomiting"
                 ,"Loss of Appetite"
                 ,"Sore Throat/Stuffy Nose"
                ],
    'Treatment': ["Antibiotic",
                "Antiviral",
                "Corticosteroid",
                "Intravenous Immunoglobin",
                "Nasal Cannula",
                "High flow nasal cannula oxygen therapy",
                "Noninvasive mechanical ventilation",
                "Invasive mechanical ventilation",
                "ECMO",
                "Glucocorticoid",
                "Renal replacement therapy"],
}

demographics = ["Median Age", "Gender"]

body = dbc.Container(
    [
        dbc.Row(
          [
            dbc.Col(
              [
              html.H1("COVID-19"),
              html.H2("Interactive Graphs")
              ]
            ),
          ],
          ),
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H5('What would you like to compare?'),
                     html.Div(dcc.Dropdown(
                         id = 'categories_dropdown',
                         options = [{'label': x, 'value': x} for x in categories],
                         value = 'Comorbidities',
                         style={'width': '80%', 'display' : 'inline-block'}),
                     ),
                     html.Div(
                        id='display-selected-values',
                        style={'width': '100%', 'display': 'inline-block','color': 'white'}),
                     html.Div([
                         html.Div(dcc.Dropdown(
                             id = 'y_axis_dropdown',
                             value = 'Current Smoker',
                             style={'width': '80%', 'display': 'inline-block'}
                             ),
                         )
                     ]),
                     html.H6('Select the Demographic (Horizontal Axis)'),
                     html.Div(dcc.Dropdown(
                         id = 'x_axis_dropdown',
                         options = [{'label': x, 'value': x} for x in demographics],
                         value = 'Gender',
                         style={'width': '80%', 'display' : 'inline-block'}),
                     ),
                   ],
                  md=4,
               ),
              dbc.Col(
                [
                    html.Div(
                    id = 'interactive_graph',
                    children = [],
                    style={
                        'width': '100%',
                        'display': 'inline-block',
                        }
                    ),
                ]
             ),
            ],
        ),
   ],
className="mt-4",
)

def App():
    layout = html.Div(
    [
        nav,
        body
    ])
    return layout

def build_graph(y_title,x_title):
    global df
    if y_title not in df.columns or x_title not in df.columns:
        return None
    cols = [x_title,y_title] + ["Survivors"]
    pre_cols = cols + ["PopSize"]
    post_cols = cols + ["Population"]
    sub_df = df[pre_cols]
    sub_df = sub_df.dropna()
    sub_df["PopSize"] = sub_df.PopSize.apply(lambda x: x.replace(',',''))
    sub_df["Population"] = sub_df.PopSize.apply(lambda x: int(x) if int(x) % 1000 == 0 else int(x) + 1000 - int(x) % 1000)
    sub_df = sub_df[post_cols]

    fig = go.Figure()
    c = 0
    colors = [
    '#1f77b4',  # muted blue
    '#9467bd',  # muted purple
    '#e377c2',  # raspberry yogurt pink
    '#2ca02c',  # cooked asparagus green
    '#ff7f0e',  # safety orange
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
    ]
    sizes = [10,20,30,40,50,60]

    for i in sub_df.Survivors.unique():
        s = 0
        for j in sub_df.Population.unique():
            fig.add_trace(go.Scatter(
                x=sub_df[(sub_df['Survivors'] == i) & (sub_df['Population'] == j)][x_title],
                y=sub_df[(sub_df['Survivors'] == i) & (sub_df['Population'] == j)][y_title],
                legendgroup=i,
                name=i+'-'+str(j),
                mode="markers",
                marker=dict(color=colors[c], size=sizes[s])
            ))
            s+=1
        c+=1

    fig.update_layout(
                height=550,
                width=730,
                title_text='<b> {} vs {} </b>'.format(x_title,y_title),
                title_font_size=25,
                xaxis={'title': x_title},
                yaxis={'title': y_title},
                legend_title='<b> Survivors-Population </b>',
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest')


    graph = dcc.Graph(
        id='interactive-graph',
        figure=fig
    )
    return graph
