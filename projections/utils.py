import pandas as pd

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

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



def get_df_projections():
    df_projections = pd.read_csv('data/predicted/Global.csv', sep=",", parse_dates = ['Day'])
    df_projections.loc[:,'Day'] = pd.to_datetime(df_projections['Day'], format='y%m%d').dt.date
    today = pd.Timestamp('today')
    df_projections = df_projections.loc[df_projections['Day']>=today]
    return df_projections


def build_notes_content(visible):
    return dbc.Card(
            style={"maxHeight": "0px"},
            id="projection-notes-card",
            className='elevation-3 projections-notes',
            children=[dbc.CardBody([
                dcc.Markdown('''**Note: The model has been updated on 7/4/2020 to better reflect the resurgence of \
                       cases in various locations. The projections could differ significantly from previous results in certain areas.** '''),
                html.H5("Note: what do we mean by \"active cases\"?"),
                dcc.Markdown("We define a COVID-19 case as **active** \
                        if it has not yet resulted in recovery \
                        or death. You may notice a discrepancy \
                        between the number of active cases here \
                        and on the \
                        [JHU map](https://coronavirus.jhu.edu/map.html). \
                        The JHU map is very good at keeping track of new cases, \
                        but does not always publish data on recovered cases, \
                        which can lead to overestimating currently active \
                        cases."),
                dcc.Markdown("**Disclaimer:** Our total counts only account for \
                        countries in which we have sufficient data and where \
                        the pandemic is currently active. In particular, it \
                        excludes some East Asian countries where the pandemic \
                        has largely passed.\n \
                        \nCountry-level projections are modelled based on all \
                        historical data to increase the accuracy of future \
                        predictions. As such, daily counts extracted from \
                        the model may not exactly correspond with reports."),
            ])],
    )
