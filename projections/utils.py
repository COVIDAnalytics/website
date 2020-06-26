import pandas as pd

import dash_bootstrap_components as dbc

def get_cols():
    return {
            'Total Detected':0,
            'Active':1,
            'Active Hospitalized':2,
            'Cumulative Hospitalized':3,
            'Total Detected Deaths':4
            }

def get_world_map_text():
    return "* Note and Disclaimer: These Plotly maps are only proposed to give an \
            approximate visual of the expansion of the disease.  \
            Borders are by definition subject to change, debate and dispute. \
            Plotly includes data from Natural Earth and defers to \
            the Natural Earth policy regarding disputed borders. \
            Grey countries correspond to those that currently have insufficient \
            data for projections or those in which the outbreak has largely passed."

def add_cases(w):
    if 'Deaths' not in w:
        w += ' Cases'
    return w

def build_card(id):
    return dbc.Col(
                [
                dbc.Card(
                    [],
                    id = id,
                    color="dark",
                    inverse=True,
                    style={'marginBottom':20,'paddingTop':20,"height":"12rem"},
                    ),
                ],
                xs=12,
                sm=6,
                md=6,
                lg=3,
            )
def get_df_projections():
    df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates = ['Day'])
    df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
    today = pd.Timestamp('today')
    df_projections = df_projections.loc[df_projections['Day']>=today]
    return df_projections
