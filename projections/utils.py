import pandas as pd
import datetime
import urllib

import dash_bootstrap_components as dbc

df_projections = pd.read_csv('data/predicted/Global_20200414.csv', sep=",", parse_dates = ['Day'])
today = pd.Timestamp('today')
oneWeekFromNow = datetime.date.today() + datetime.timedelta(days=7)

df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
df_projections = df_projections.loc[df_projections['Day']>=today]
df_us = df_projections.loc[(df_projections.Country == "US") & (df_projections.Province != 'None')]

cols={'Total Detected':0,'Active':1,'Active Hospitalized':2,
                'Cumulative Hospitalized':3,'Total Detected Deaths':4};

map_locations = ['US', "Europe", "Asia", "North America", "South America", "Africa", 'World']

dataset = "data/predicted/Global_20200412.csv"
data_csv_string = df_projections.to_csv(index=False, encoding='utf-8')
data_csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(data_csv_string)

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
