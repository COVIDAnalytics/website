import pandas as pd
import datetime
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc

from ventilators.utils import df_mod1_shortages, df_mod1_transfers,df_mod1_projections
from ventilators.utils import df_mod2_shortages, df_mod2_transfers,df_mod2_projections
from ventilators.utils import us_map, us_timeline, no_model_visual, model_visual

def build_transfers_map(chosen_model,chosen_date,p1,p2,p3):
    global df_mod1_shortages
    global df_mod2_shortages
    if chosen_model == "Washington IHME":
        df_map = df_mod1_shortages.copy()
    else:
        df_map = df_mod2_shortages.copy()

    df_map = df_map.loc[df_map.Param1==float(p1)]
    df_map = df_map.loc[df_map.Param2==float(p2)]
    df_map = df_map.loc[df_map.Param3==float(p3)]

    return us_map(df_map,chosen_date,"Shortage",model_visual)

def build_transfers_timeline(chosen_model,p1,p2,p3):
    global df_mod1_shortages
    global df_mod2_shortages
    global df_mod1_projections
    global df_mod2_projections
    if chosen_model == "Washington IHME":
        df_opt_pre = df_mod1_projections.copy()
        df_opt_post = df_mod1_shortages.copy()
    else:
        df_opt_pre = df_mod2_projections.copy()
        df_opt_post = df_mod1_shortages.copy()

    timeline_cols = ["Date","Shortage"]
    df_opt_pre = df_opt_pre.loc[df_opt_pre.State == 'US']
    df_opt_pre = df_opt_pre[timeline_cols]
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

def build_transfer_options(chosen_model,chosen_date,to_or_from,p1,p2,p3):
    global df_mod1_transfers
    global df_mod2_transfers
    if chosen_model == "Washington IHME":
        df_trans = df_mod1_transfers
    else:
        df_trans = df_mod2_transfers
    if isinstance(chosen_date, str):
        chosen_date = datetime.datetime.strptime(chosen_date, '%Y-%m-%d').date()

    df_trans = df_trans.loc[df_trans['Date']==chosen_date]
    df_trans = df_trans.loc[df_trans.Param1==float(p1)]
    df_trans = df_trans.loc[df_trans.Param2==float(p2)]
    df_trans = df_trans.loc[df_trans.Param3==float(p3)]

    if to_or_from == "to":
        return [{'label': x, 'value': x} for x in sorted(df_trans.State_To.unique())]
    else:
        return [{'label': x, 'value': x} for x in sorted(df_trans.State_From.unique())]

def build_transfers_table(chosen_model,chosen_date,to_or_from,state,p1,p2,p3):
    global df_mod1_transfers
    global df_mod2_transfers

    if chosen_model == "Washington IHME":
        df_trans = df_mod1_transfers.copy()
    else:
        df_trans = df_mod2_transfers.copy()
    if isinstance(chosen_date, str):
        chosen_date = datetime.datetime.strptime(chosen_date, '%Y-%m-%d').date()
    df_trans = df_trans.loc[df_trans['Date']==chosen_date]
    df_trans = df_trans.loc[df_trans.Param1==float(p1)]
    df_trans = df_trans.loc[df_trans.Param2==float(p2)]
    df_trans = df_trans.loc[df_trans.Param3==float(p3)]

    if to_or_from == "to":
        df_trans = df_trans.loc[df_trans['State_To']==state]
        df_trans = df_trans[["State_From","Num_Units"]]
        df_trans.columns = ["State","Units"]
    else:
        df_trans = df_trans.loc[df_trans['State_From']==state]
        df_trans = df_trans[["State_From","Num_Units"]]
        df_trans.columns = ["State","Units"]

    tab_transfers = dash_table.DataTable(
            id="transfer_list",
            data=df_trans.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_trans.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_table={
                'overflow':'auto',
                'maxHeight': '300px',
                'maxWidth': '500px',
                'border': 'thin lightgrey solid',
            },
            style_cell={
                'height': 'auto',
                'minWidth': '0px',
                'width': '50px',
                'maxWidth': '180px',
                'whiteSpace': 'normal',
                'textAlign': 'center',
                'font_size': '14px',
                'font-family': 'arial',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'display': 'none',
            }
        )
    return df_trans.to_dict('records')
