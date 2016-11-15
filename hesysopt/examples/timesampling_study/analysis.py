
# coding: utf-8

import seaborn as sns
import pandas as pd
from hesysopt.restore_results import restore
from scenario_builder import scenarios
import postprocessing as pp


main_df, colors = restore(list(scenarios.keys()))
idx = pd.IndexSlice
heat_df = main_df.loc[idx['heat_balance','to_bus',:,:,:]].unstack(['Scenario', 'obj_label'])
heat_df.columns = heat_df.columns.droplevel([0])
el_df = main_df.loc[idx['electrical_balance', 'to_bus', :, :, :]].unstack(['Scenario', 'obj_label'])
el_df.columns = el_df.columns.droplevel([0])



for i in scenarios.keys():
    pp.summed_production(heat_df[i],
                         colors=colors['components'])

if False:
    el_df.columns = el_df.columns.swaplevel(0,1)
    BP1 = el_df.ix[:, 'BP1']
    pp.sorted_curves(BP1, colors['scenarios'])

    heat_df.columns = heat_df.columns.swaplevel(0,1)
    OB = heat_df.ix[:,'OB']
    pp.sorted_curves(OB, colors['scenarios'])