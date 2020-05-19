from ventilators.utils import get_df_mod1_projections, get_df_mod2_projections
from ventilators.utils import us_map, us_timeline, get_no_model_visual

# Build the map of current demand, supply, and shortage
def build_shortage_map(chosen_model,chosen_date,val):
    if chosen_model == "Washington IHME":
        df_map,_ = get_df_mod1_projections()
    else:
        df_map = get_df_mod2_projections()
    no_model_visual = get_no_model_visual()
    return us_map(df_map,chosen_date,val,no_model_visual)

# Build the US timeline of current demand, supply, and shortage
def build_shortage_timeline(chosen_model):
    if chosen_model == "Washington IHME":
        df_projections_vent_us,_ = get_df_mod1_projections()
    else:
        df_projections_vent_us = get_df_mod2_projections()

    df_projections_vent_us = df_projections_vent_us.loc[df_projections_vent_us.State == 'US']

    return us_timeline(df_projections_vent_us, "US Ventilator Supply, Demand, & Shortage", False)
