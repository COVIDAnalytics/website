import datetime
import numpy as np
import plotly.graph_objects as go
from textwrap import wrap

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from assets.mappings import get_states, get_colors
from projections.map import build_card_content
from projections.utils import get_cols, add_cases

def build_continent_map(df_continent,PopInfo,map_date,val='Active', continent = 'World', pop = 1):
    if continent !='World':
        df_continent = df_continent.loc[df_continent.Continent == continent] #Filter by continent

    if map_date is None:
        return None

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date()

    df_map = df_continent.loc[df_continent['Day'] == map_date]
    df_map = df_map.loc[df_map['Province'] == 'None'] #exclude province data
    df_map = df_map.loc[df_map['Country'] != 'None'] #exclude global world data

    population = np.array([])
    for i in df_map['Country']:
        ind1 = np.logical_and(PopInfo['Country']==i, PopInfo['Province']=='None')
        pop_val = PopInfo.loc[ind1,'pop'].values
        population = np.concatenate((population, pop_val),0)

    df_map['Population'] =population

    df_map['Active Per Million'] = (np.round(1000000*df_map['Active']/df_map['Population'], decimals = 2))
    df_map['Total Detected Per Million'] = (np.round(1000000*df_map['Total Detected']/df_map['Population'], decimals = 2))
    df_map['Active Hospitalized Per Million'] = (np.round(1000000*df_map['Active Hospitalized']/df_map['Population'], decimals = 2))
    df_map['Cumulative Hospitalized Per Million'] = (np.round(1000000*df_map['Cumulative Hospitalized']/df_map['Population'], decimals = 2))
    df_map['Total Detected Deaths Per Million'] = (np.round(1000000*df_map['Total Detected Deaths']/df_map['Population'], decimals = 2))
    df_map = df_map.applymap(str)

    cols = get_cols()
    if (val is not None) and (val in cols) and  pop == 1:

        df_map.loc[:,'text'] = df_map['Country'] + '<br>' + \
                    'Total Detected ' + df_map['Total Detected'] + '<br>' + \
                    'Active ' + df_map['Active'] + '<br>' + \
                    'Active Hospitalized ' + df_map['Active Hospitalized'] + '<br>' + \
                    'Cumulative Hospitalized ' + df_map['Cumulative Hospitalized'] + '<br>' + \
                    'Total Detected Deaths ' + df_map['Total Detected Deaths']
        zval = df_map[val].astype(float)

    if (val is not None) and (val in cols) and  pop != 1:

        df_map.loc[:,'text'] = df_map['Country'] + '<br>' + \
                    'Total Detected Per Million ' + df_map['Total Detected Per Million'] + '<br>' + \
                    'Active Per Million ' + df_map['Active Per Million'] + '<br>' + \
                    'Active Hospitalized Per Million ' + df_map['Active Hospitalized Per Million'] + '<br>' + \
                    'Cumulative Hospitalized Per Million ' + df_map['Cumulative Hospitalized Per Million'] + '<br>' + \
                    'Total Detected Deaths Per Million ' + df_map['Total Detected Deaths Per Million']


        zval = df_map[val+ " Per Million"].astype(float)

    if (val is not None) and (val in cols):
        fig = go.Figure(data=go.Choropleth(
            locations=df_map['Country'],
            z= zval,
            locationmode="country names",
            autocolorscale=False,
            colorscale='inferno_r',
            text=df_map['text'], # hover text
            marker_line_color='black', # line markers between states
            colorbar_title='<br>'.join(wrap(''.join(['{}'.format(add_cases(val))]), width=10))
        ))

        fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=50),
                title_text=add_cases('{} Predicted {} {}'.format(map_date.strftime('%b %d,%Y'), continent, val)),
                geo = dict(
                    scope= continent.lower() if continent is not None else None,
                    projection=go.layout.geo.Projection(type = 'natural earth'),
                    showlakes=True, # lakes
                    lakecolor='rgb(255, 255, 255)',
                    countrycolor='lightgray',
                    landcolor='whitesmoke',
                    showland=True,
                    showframe = False,
                    showcoastlines = True,
                    showcountries=True,
                    visible = False,
                ),
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )

        graph = dcc.Graph(
            id='continent-projection-map',
            figure=fig,
        )

        return graph
    return


def build_us_map(df_projections,PopInfo,map_date,val='Active', pop = 1):
    if map_date is None:
        return None

    if isinstance(map_date, str):
        map_date = datetime.datetime.strptime(map_date, '%Y-%m-%d').date()

    df_us = df_projections.loc[(df_projections.Country == "US") & (df_projections.Province != 'None')]
    df_map = df_us.loc[df_us['Day']==map_date]
    df_map = df_map.loc[df_us['Province']!='US']

    states = get_states()
    df_map.loc[:,'code'] = df_map.Province.apply(lambda x: states[x])
    population = np.array([])

    for i in df_map['Province']:
        pop_val = PopInfo.loc[PopInfo['Province']==i,'pop'].values
        population = np.concatenate((population, pop_val),0)

    df_map['Population'] =population
    df_map['Active Per Million'] = (np.round(1000000*df_map['Active']/df_map['Population'], decimals = 2))
    df_map['Total Detected Per Million'] = (np.round(1000000*df_map['Total Detected']/df_map['Population'], decimals = 2))
    df_map['Active Hospitalized Per Million'] = (np.round(1000000*df_map['Active Hospitalized']/df_map['Population'], decimals = 2))
    df_map['Cumulative Hospitalized Per Million'] = (np.round(1000000*df_map['Cumulative Hospitalized']/df_map['Population'], decimals = 2))
    df_map['Total Detected Deaths Per Million'] = (np.round(1000000*df_map['Total Detected Deaths']/df_map['Population'], decimals = 2))
    df_map = df_map.applymap(str)

    cols = get_cols()
    if (val is not None) and (val in cols) and pop == 1:

        df_map.loc[:,'text'] = df_map['Province'] + '<br>' + \
                    'Total Detected ' + df_map['Total Detected'] + '<br>' + \
                    'Active ' + df_map['Active'] + '<br>' + \
                    'Active Hospitalized ' + df_map['Active Hospitalized'] + '<br>' + \
                    'Cumulative Hospitalized ' + df_map['Cumulative Hospitalized'] + '<br>' + \
                    'Total Detected Deaths ' + df_map['Total Detected Deaths']

        z_val = df_map[val].astype(float)


    if (val is not None) and (val in cols) and pop != 1:

        df_map.loc[:,'text'] = df_map['Province'] + '<br>' + \
            'Total Detected Per Million ' + df_map['Total Detected Per Million'] + '<br>' + \
            'Active Per Million ' + df_map['Active Per Million'] + '<br>' + \
            'Active Hospitalized Per Million ' + df_map['Active Hospitalized Per Million'] + '<br>' + \
            'Cumulative Hospitalized Per Million ' + df_map['Cumulative Hospitalized Per Million'] + '<br>' + \
            'Total Detected Deaths Per Million ' + df_map['Total Detected Deaths Per Million']
        z_val =df_map[val+ " Per Million"].astype(float)

    if (val is not None) and (val in cols):
        fig = go.Figure(data=go.Choropleth(
            locations=df_map['code'],
            z=z_val,
            locationmode='USA-states',
            colorscale='inferno_r',
            autocolorscale=False,
            text=df_map['text'], # hover text
            marker_line_color='white' , # line markers between states
            colorbar_title='<br>'.join(wrap(''.join(['{}'.format(add_cases(val))]), width=10))
        ))


        fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=50),
                title_text=add_cases('{} Predicted US {}'.format(map_date.strftime('%b %d,%Y'), val)),
                geo = dict(
                    scope='usa',
                    projection=go.layout.geo.Projection(type = 'albers usa'),
                    showlakes=True, # lakes
                    lakecolor='rgb(255, 255, 255)'
                ),
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )

        graph = dcc.Graph(
            id='us-projection-map',
            figure=fig
        )
        return graph
    return

def find_smallest_scope(state, country, continent):
    location = state
    if state in 'None':
        if country in 'None':
            location = continent
        else:
            location = country
    return location

def build_state_projection(df_projections, state, country, continent, vals):
    location = find_smallest_scope(state, country, continent)
    print("LOcation is : " + location)
    df_projections_sub = df_projections.loc[ (df_projections.Province == state) & (df_projections.Country == country)]
    if continent not in ['US', 'World']:
        df_projections_sub = df_projections_sub.loc[(df_projections_sub.Continent == continent)]
    if continent == 'US':
        df_projections_sub = df_projections.loc[(df_projections.Country == 'US') & (df_projections.Province == state)]
    if continent == 'World':
        if country =='None':
            df_projections_sub = df_projections.loc[(df_projections.Continent == 'None')] #include only global world data
    fig = go.Figure()

    cols = get_cols()
    if (vals is not None) and (set(vals).issubset(set(cols))):
        colors = get_colors()
        for val in vals:
            i = cols[val]
            fig.add_trace(go.Scatter(
                name=val,
                showlegend=True,
                x=df_projections_sub['Day'],
                y=df_projections_sub[val].values,
                mode="lines",
                marker=dict(color=colors[i]),
                line=dict(color=colors[i])
            ))

    title = '<br>'.join(wrap('<b> Projections for {} </b>'.format(location), width=26))
    fig.update_layout(
                height=550,
                title={
                    'text': title,
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                title_font_size=25,
                xaxis={'title': "Date",'linecolor': 'lightgrey'},
                yaxis={'title': "Count",'linecolor': 'lightgrey'},
                legend_title='<b> Values Predicted </b>',
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend={
                        "orientation": "h",
                        "xanchor": "center",
                        "y": -0.2,
                        "x": 0.5
                        },
                modebar={
                    'orientation': 'v',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'color': 'lightgray',
                    'activecolor': 'gray'
                }
            )

    graph = dcc.Graph(
        id='projection-graph',
        figure=fig
    )
    return graph


def get_stat(df_projections, d, val, scope):
    if d is None:
        return None
    if isinstance(d, str):
        d = datetime.datetime.strptime(d, '%Y-%m-%d').date()
    if scope == 'US':
        df_projections_sub = df_projections.loc[(df_projections.Country == scope) & (df_projections.Province == 'None')]
    elif scope =='World':
        df_projections_sub = df_projections.loc[df_projections.Continent == 'None']
    else:
        df_projections_sub = df_projections.loc[(df_projections.Continent == scope) & (df_projections.Country == 'None')]

    df_projections_sub = df_projections_sub.loc[df_projections_sub['Day']==d].reset_index()

    if df_projections_sub.empty:
        return None

    if val != "Active Hospitalized":
        t = add_cases(val)
    else:
        t = val
    return build_card_content(f'{df_projections_sub.iloc[0][val]:,}', t)
