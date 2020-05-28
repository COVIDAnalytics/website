import pandas as pd
import urllib
import plotly.graph_objects as go
from textwrap import wrap
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from footer import Footer
from assets.mappings import get_colors

def InteractiveGraph():
    nav = Navbar()
    footer = Footer()

    categories = ["Comorbidities","Symptoms","Treatment","Lab Test Results"]

    demographics = ["Median Age", "% Male"]
    df = pd.read_csv('data/clinical_outcomes_database.csv')
    survivor_options = df.Survivors.unique()
    data_csv_string = df.to_csv(index=False, encoding='utf-8')
    data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)
    del df
    survivor_options = [x for x in survivor_options if str(x) != 'nan']

    body = dbc.Container(
        [
            dbc.Row(
            [
                dbc.Col(
                [
                  html.H2("Insights")
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
                    html.Div(
                        dcc.Dropdown(
                            id = 'categories_dropdown',
                            options = [{'label': x, 'value': x} for x in categories],
                            value = 'Comorbidities',
                            style={'marginBottom': 10}
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
                                optionHeight = 50,
                                style={'marginBottom': 10,'marginTop': 10}
                            ),
                        )
                    ]
                    ),
                    html.P('Select the Demographic (Horizontal Axis)'),
                    html.Div(
                        dcc.Dropdown(
                            id = 'x_axis_dropdown',
                            options = [{'label': x, 'value': x} for x in demographics],
                            value = '% Male',
                            style={'marginBottom': 10,'marginTop': -5}
                        ),
                    ),
                    html.P('Select the Population Type:'),
                    html.Div(
                    dcc.Checklist(
                        id = 'survivors',
                        options=[{'label': x, 'value': x} for x in survivor_options],
                        value=['Non-survivors only', 'Survivors only'],
                        labelStyle={'color': 'black'},
                        style={'width': '50%','marginTop': -5}
                        )
                    ),
                ],
                width="True",
                ),
            ],
            justify="center"
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
                            target="_blank"                        ),
                        style={'textAlign':"center"}
                    )
                ),
                ]
            ),
       ],
       className="page-body",
    )

    layout = html.Div([nav, body, footer],className="site")
    return layout

def graph_bucket(x,buckets):
    numBuckets = len(buckets)
    b = 0
    while b < numBuckets and x > buckets[b]:
        b+=1
    # b should never be == numBuckets but just in case
    return buckets[b] if b < numBuckets else max_pop

def get_lb(ind,buckets):
    return str(buckets[ind-1]) if ind > 0 else '0'


def build_graph(df,y_title,x_title,survivor_vals):
    if y_title not in df.columns or x_title not in df.columns:
        return None
    cols = [x_title,y_title] + ["Survivors","Country"]
    pre_cols = cols + ["Study Pop Size (N)"]
    post_cols = cols + ["Population"]
    df = df[pre_cols]
    df = df.dropna()
    max_pop = max(df["Study Pop Size (N)"].values)
    #round up the maximum number to the nearest hundred
    max_pop = int(max_pop) + 100 - int(max_pop) % 100
    buckets = [100,500,1000,2000,max_pop]
    df["Population"] = df["Study Pop Size (N)"].apply(lambda x: graph_bucket(x,buckets))
    df = df[post_cols]
    df = df[df['Survivors'].isin(survivor_vals)]


    colors = get_colors()
    fig = go.Figure()
    color_ind = {'Non-survivors only':1,'Survivors only':4,'Both':2}
    sizes = [5,10,20,40,60]
    for i in df.Survivors.unique():
        s = 0
        for ind,j in enumerate(buckets):
            fig.add_trace(go.Scatter(
                x=df[(df['Survivors'] == i) & (df['Population'] == j)][x_title],
                y=df[(df['Survivors'] == i) & (df['Population'] == j)][y_title],
                legendgroup=i,
                name= '{} <br> {} < Pop. Size < {}'.format(i, get_lb(ind,buckets),str(int(j))),
                mode="markers",
                marker=dict(color=colors[color_ind[i]], size=sizes[ind]),
                text=df['Country'],
            ))
            s+=1

    fig.update_layout(
                height=550,
                title={
                    'text': '<br>'.join(wrap('<b> {} vs {} </b>'.format(x_title,y_title), width=26)),
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
                plot_bgcolor='rgba(0,0,0,0)',
                legend={
                        "orientation": "h",
                        "xanchor": "center",
                        "y": -0.2,
                        "x": 0.5,
                        "itemsizing":"trace"
                        },
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )


    graph = dcc.Graph(
        id='interactive-graph',
        figure=fig
    )
    return graph
