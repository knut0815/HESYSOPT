
# coding: utf-8

import seaborn as sns
import pandas as pd
from hesysopt.restore_results import restore
from scenario_builder import all_scenarios
import postprocessing as pp


results, scenarios, colors = restore(list(all_scenarios.keys()))
main_df = results['dispatch']
idx = pd.IndexSlice
heat_df = main_df.loc[idx['heat_balance','to_bus',:,:,:]].unstack(['Scenario',
                                                                   'obj_label'])
heat_df.columns = heat_df.columns.droplevel([0])
el_df = main_df.loc[idx['electrical_balance', 'to_bus', :, :, :]].unstack(['Scenario',
                                                                           'obj_label'])
el_df.columns = el_df.columns.droplevel([0])


#for i in scenarios.keys():
#    pp.summed_production(heat_df[i],
#                         colors=colors['components'])


select = [i for i in all_scenarios.keys() if '10MWh' in i]
#select = [i for i in all_scenarios.keys()]
if False:
    el_df.columns = el_df.columns.swaplevel(0,1)
    el_df.sort_index(axis=1, inplace=True)
    BP1 = el_df.loc[:, idx['BP1', select]]
    pp.sorted_curves(BP1, colors['scenarios'])
if True:
    heat_df.columns = heat_df.columns.swaplevel(0,1)
    OB = heat_df.ix[:,'OB']
    pp.sorted_curves(OB, colors['scenarios'])

if True:
    x = el_df.unstack().unstack('obj_label')
    x.fillna(method='ffill', inplace=True)

df = pp.compare_objectives(results['objective'], None)