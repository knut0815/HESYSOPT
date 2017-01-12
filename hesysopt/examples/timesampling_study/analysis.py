
# coding: utf-8

import seaborn as sns
import pandas as pd
from hesysopt.restore_results import restore
from scenario_builder import all_scenarios
import postprocessing as pp


select = [i for i in all_scenarios.keys()]

results, scenarios, colors = restore(select)
main_df = results['dispatch']

idx = pd.IndexSlice
heat_df = main_df.loc[idx['heat_balance','to_bus',:,:,:]].unstack(['Scenario',
                                                                   'obj_label'])
heat_df.columns = heat_df.columns.droplevel([0])
storage_df = main_df.loc[idx['heat_balance','other',:,:,:]].unstack(['Scenario',
                                                                   'obj_label'])
storage_df.columns = storage_df.columns.droplevel([0])

el_df = main_df.loc[idx['electrical_balance', 'to_bus', :, :, :]].unstack(['Scenario',
                                                                           'obj_label'])
el_df.columns = el_df.columns.droplevel([0])


#for i in scenarios.keys():
#    pp.summed_production(heat_df[i],
#                         colors=colors['components'])

ax = heat_df[select[4]].iloc[2000:2168].plot(stacked=True)
storage_df[select[4]].iloc[2000:2168].plot(ax=ax, color='black', drawstyle='steps')

sub_select = select
if False:
    el_df.columns = el_df.columns.swaplevel(0,1)
    el_df.sort_index(axis=1, inplace=True)
    BP1 = el_df.loc[:, idx['BP1', select]]
    pp.sorted_curves(BP1, colors['scenarios'])

if True:
    temp_df = heat_df.copy()
    temp_df.columns = temp_df.columns.swaplevel(0,1)
    temp_df.sort_index(axis=1, inplace=True)
    OB = temp_df.loc[:, idx['BP1', sub_select]]
    pp.sorted_curves(OB, colors['scenarios'])

if False:
    x = el_df.unstack().unstack('obj_label')
    x.fillna(method='ffill', inplace=True)

if False:
    df = pp.compare_objectives(results['objective'], None)