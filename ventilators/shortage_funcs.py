from ventilators.utils import df_mod1_shortages, df_mod1_transfers,df_mod1_projections
from ventilators.utils import df_mod2_shortages, df_mod2_transfers,df_mod2_projections
from ventilators.utils import us_map, us_timeline, no_model_visual, model_visual

# Build the map of current demand, supply, and shortage
def build_shortage_map(chosen_model,chosen_date,val):
    global df_mod1_projections
    global df_mod2_projections
    if chosen_model == "Washington IHME":
        df_map = df_mod1_projections.copy()
    else:
        df_map = df_mod2_projections.copy()

    return us_map(df_map,chosen_date,val,no_model_visual)

# Build the US timeline of current demand, supply, and shortage
def build_shortage_timeline(chosen_model):
    global df_mod1_projections
    global df_mod2_projections
    if chosen_model == "Washington IHME":
        df_projections_vent_us = df_mod1_projections.copy()
    else:
        df_projections_vent_us = df_mod2_projections.copy()

    return us_timeline(df_projections_vent_us,no_model_visual, "US Ventilator Supply and Demand")
