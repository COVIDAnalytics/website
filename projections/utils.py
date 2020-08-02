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
    return dbc.Card(
        className="elevation-3",
        style={
            "marginTop": "30px",
            "padding": "20px",
            "border": "none",
        },
        children=html.P(
            style={ "color": "grey", "margin": "0px" },
            children="* Note and Disclaimer: These Plotly maps are only proposed to give an \
            approximate visual of the expansion of the disease.  \
            Borders are by definition subject to change, debate and dispute. \
            Plotly includes data from Natural Earth and defers to \
            the Natural Earth policy regarding disputed borders. \
            Grey countries correspond to those that currently have insufficient \
            data for projections or those in which the outbreak has largely passed."))

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


def get_state_abbr(reverse=False):
    states = {
        # us states
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands':'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
        # Canada states
        'Alberta': 'AB',
        'British Columbia': 'BC',
        'Manitoba': 'MB',
        'New Brunswick': 'NB',
        'Newfoundland and Labrador': 'NL',
        'Northwest Territories': 'NT',
        'Nova Scotia': 'NS',
        'Nunavut': 'NU',
        'Ontario': 'ON',
        'Prince Edward Island': 'PE',
        'Quebec': 'QC',
        'Saskatchewan': 'SK',
        'Yukon': 'YT',
        # Australia states
        'New South Wales': 'NSW',
        'Northern Territory': 'NT',
        'Queensland': 'Qld',
        'South Australia': 'SA',
        'Tasmania': 'Tas',
        'Victoria': 'Vic',
        'Western Australia': 'WA',
        'Australian Capital Territory': 'ACT',
        # None
        'None': 'All'
    }
    if reverse:
        states = dict(map(reversed, states.items()))
    return states