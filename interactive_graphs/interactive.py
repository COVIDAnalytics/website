### Data
import pandas as pd
from datetime import datetime as dt
import urllib
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer
from assets.mappings import colors

dataset = "data/clinical_outcomes_database.csv"
df = pd.read_csv('data/clinical_outcomes_database.csv')
data_csv_string = df.to_csv(index=False, encoding='utf-8')
data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)

nav = Navbar()
footer = Footer()

categories = ["Comorbidities","Symptoms","Treatment"]

demographics = ["Median Age", "% Male"]

survivor_options = df.Survivors.unique()
survivor_options = [x for x in survivor_options if str(x) != 'nan']

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
              html.H2("Interactive Graphs")
            ]
            ),
        ],
        ),
        dbc.Row(
        [
            dbc.Col(
            [
                html.Div(
                [
                    dcc.Markdown(
                         """\
                            Effective decision making needs data. \
                            We interactively visualize a new [dataset](/dataset) \
                            that aggregates data from over 100 published clinical \
                            studies and preprints released between December 2019 \
                            and March 2020 on COVID-19. We hope that by summarizing\
                            the results of multiple studies, we can get a clearer \
                            picture on the virus.
                         """,
                    ),
                    html.P(
                         """\
                            Below you will find a series of \
                            options to create descriptive graphs relating to patient \
                            demographic characteristics, symptoms, treatments, \
                            comorbidities, lab results, and outcomes. \
                            Each data point corresponds to a different study that \
                            comprises multiple patients. We hope that you can easily \
                            derive your own insights and discover the interesting \
                            implications of the disease.
                         """,
                    )
                ]
                )
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
                    ),
                ),
                html.Div(
                    id='display-selected-values',
                    ),
                html.Div([
                    html.Div(
                        dcc.Dropdown(
                            id = 'y_axis_dropdown',
                            value = 'Hypertension',
                        ),
                    )
                ]
                ),
                html.H6('Select the Demographic (Horizontal Axis)'),
                html.Div(dcc.Dropdown(
                    id = 'x_axis_dropdown',
                    options = [{'label': x, 'value': x} for x in demographics],
                    value = '% Male',
                    ),
                ),
                html.H6('Select the Population Type:'),
                html.Div(
                dcc.Checklist(
                    id = 'survivors',
                    options=[{'label': x, 'value': x} for x in survivor_options],
                    value=['Non-Survivors only', 'Survivors only'],
                    labelStyle={'color': 'black'},
                    style={'width': '50%'}
                    )
                ),
            ],
            width="True",
            align="center"
            ),
        ],
        ),
        dbc.Row(
            [
            dbc.Col(
            [
                html.Div(
                    id = 'interactive_graph',
                    children = [],
                    ),
            ]
            ),
            ]
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.A(
                        "Download the Data",
                        id="download-link",
                        download="covid_analytics_clinical_data.csv",
                        href=data_csv_string,
                        target="_blank"
                    ),
                    style={'text-align':"center"}
                )
            ),
            ]
        ),
   ],
   className="page-body",
)

def InteractiveGraph():
    layout = html.Div([nav, body, footer],className="site")
    return layout

def build_graph(y_title,x_title,survivor_vals):
    global df
    if y_title not in df.columns or x_title not in df.columns:
        return None
    cols = [x_title,y_title] + ["Survivors","Country"]
    pre_cols = cols + ["Study Pop Size (N)"]
    post_cols = cols + ["Population"]
    sub_df = df[pre_cols]
    sub_df = sub_df.dropna()
    sub_df["Population"] = sub_df["Study Pop Size (N)"].apply(lambda x: int(x) if int(x) % 1000 == 0 else int(x) + 1000 - int(x) % 1000)
    sub_df = sub_df[post_cols]
    sub_df = sub_df[sub_df['Survivors'].isin(survivor_vals)]

    fig = go.Figure()
    c = 0
    sizes = [10,20,30,40,50,60]
    for i in sub_df.Survivors.unique():
        s = 0
        for j in sub_df.Population.unique():
            fig.add_trace(go.Scatter(
                x=sub_df[(sub_df['Survivors'] == i) & (sub_df['Population'] == j)][x_title],
                y=sub_df[(sub_df['Survivors'] == i) & (sub_df['Population'] == j)][y_title],
                legendgroup=i,
                name= '{} <br> {}K < Pop. Size < {}K'.format(i,str(int((j-1000)/1000)),str(int(j/1000))),
                mode="markers",
                marker=dict(color=colors[c], size=sizes[s]),
                text=sub_df['Country'],
            ))
            s+=1
        c+=1

    fig.update_layout(
                height=550,
                title={
                    'text': '<b> {} vs {} </b>'.format(x_title,y_title),
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=20,
                xaxis={'title': x_title,'linecolor': 'lightgrey'},
                yaxis={'title': "Percentage with " + y_title,'linecolor': 'lightgrey'},
                legend_title='<b> Survivors <br> Population Size </b>',
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )


    graph = dcc.Graph(
        id='interactive-graph',
        figure=fig
    )
    return graph
