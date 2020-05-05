import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

map_time = {
    0: "Now",
    1: "One Week",
    2: "Two Weeks",
    3: "Four Weeks",
    4: "Six Weeks"
}

name_to_json = {
    "No Restrictions": "No_Measure",
    "Lockdown":"Lockdown",
    "Restrict Mass Gatherings and Schools": "Restrict_Mass_Gatherings_and_Schools",
    "Restrict Mass Gatherings": "Restrict_Mass_Gatherings",
    "Restrict Non-Essential Businesses, Travel Restriction and Workplaces": "Mass_Gatherings_Authorized_But_Others_Restricted",
    "Restrict Mass Gatherings, Non-Essential Businesses, Travel Restriction and Workplaces": "Authorize_Schools_but_Restrict_Mass_Gatherings_and_Others",
    "Restrict Mass Gatherings, Schools, Non-Essential Businesses, Travel Restriction and Workplaces": "Restrict_Mass_Gatherings_and_Schools_and_Others"
}

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
