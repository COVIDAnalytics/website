import datetime

import dash_bootstrap_components as dbc
import dash_html_components as html

def map_policy(vec):
    if vec[0]:
        return "No Restrictions"
    if vec[1]:
        return "Lockdown"
    if vec[2]:
        if vec[3]:
            if vec[4]:
                return "Restrict Mass Gatherings, Schools, Non-Essential Businesses, Travel Restriction and Workplaces"
            else:
                return "Restrict Mass Gatherings and Schools"
        elif vec[4]:
                return "Restrict Mass Gatherings, Non-Essential Businesses, Travel Restriction and Workplaces"
        else:
            return "Restrict Mass Gatherings"
    return "Restrict Non-Essential Businesses, Travel Restriction and Workplaces"

def no_policy_chosen(policies):
    for policy in policies:
        if sum(policy) > 0:
            return False
    return True

def get_projections():
    return \
    [
         dbc.Row(
         [
               dbc.Col(
               [
                     html.Div(
                         id = 'policy_projection_graph',
                         children = [],
                         style={
                             'width': '100%',
                             'display': 'inline-block',
                             'paddingTop': 20,
                             }
                     ),
                ]
                ),
                dbc.Col(
                [
                      html.Div(
                          id = 'policy_deaths_projection_graph',
                          children = [],
                          style={
                              'width': '100%',
                              'display': 'inline-block',
                              'paddingTop': 20,
                              }
                      ),
                 ]
                 )
          ],
          )
    ]

def get_start(t):
    return datetime.date.today() + datetime.timedelta(days=7*t)
