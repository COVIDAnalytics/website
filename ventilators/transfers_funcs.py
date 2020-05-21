import pandas as pd
import datetime

import dash_html_components as html

from ventilators.utils import us_map, us_timeline, get_no_model_visual, get_model_visual

def build_transfers_map(chosen_model,chosen_date,p1,p2,p3):
    if chosen_model == "Washington IHME":
        df_map = pd.read_csv('data/predicted_ventilator/state_supplies_table-ihme.csv', sep=",", parse_dates = ['Date'])
    else:
        df_map = pd.read_csv('data/predicted_ventilator/state_supplies_table-ode.csv', sep=",", parse_dates = ['Date'])

    df_map.loc[:,'Date'] = pd.to_datetime(df_map['Date'], format='y%m%d').dt.date
    df_map = df_map.loc[df_map.Param1==float(p1)]
    df_map = df_map.loc[df_map.Param2==float(p2)]
    df_map = df_map.loc[df_map.Param3==float(p3)]
    model_visual = get_model_visual()
    return us_map(df_map,chosen_date,"Shortage",model_visual)

def build_transfers_timeline(df_opt_pre,df_opt_post,p1,p2,p3):
    df_opt_post.loc[:,'Date'] = pd.to_datetime(df_opt_post['Date'], format='y%m%d').dt.date
    timeline_cols = ["Date","Shortage"]
    df_opt_pre = df_opt_pre.loc[df_opt_pre.State == 'US']
    df_opt_pre = df_opt_pre[timeline_cols]

    no_model_visual = get_no_model_visual()
    model_visual = get_model_visual()

    df_opt_pre.columns = ["Date",no_model_visual["Shortage"]]

    df_opt_post = df_opt_post.loc[
                                    (df_opt_post.State == 'US') & \
                                    (df_opt_post.Param1==float(p1)) & \
                                    (df_opt_post.Param2==float(p2)) & \
                                    (df_opt_post.Param3==float(p3))
                                ]

    df_opt_post = df_opt_post[timeline_cols]
    df_opt_post.columns = ["Date",model_visual["Shortage"]]

    df_opt_effect = pd.merge(df_opt_pre,df_opt_post,on='Date',how='inner')

    return us_timeline(df_opt_effect,"Optimization Effect on Shortage",True)

def generate_table(df_trans,to_or_from=None,state=None):
    orig_cols = ["State_From","State_To","Num_Units"]
    final_cols = ["Origin","Destination","Units"]
    if state:
        if to_or_from == "to":
            df_trans = df_trans.loc[df_trans['State_To']==state]
        else:
            df_trans = df_trans.loc[df_trans['State_From']==state]

    df_trans = df_trans[orig_cols]
    df_trans.columns = final_cols
    max_rows = 100
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_trans.columns])] +

        # Body
        [
            html.Tr([
                html.Td(
                    df_trans.iloc[i][col]) for col in df_trans.columns
                    ]
                ) for i in range(min(len(df_trans), max_rows))
        ],
        id="transfers-table"
    )
