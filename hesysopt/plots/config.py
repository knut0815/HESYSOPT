# -*- coding: utf-8 -*-
"""
"""
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

scenarios = ['2H_sample']
homepath = os.path.expanduser('~')

main_df = pd.DataFrame()
for s in scenarios:
    resultspath = os.path.join(homepath, 'hesysopt_simulation', s, 'results',
                               'all_results.csv')
    tmp = pd.read_csv(resultspath)
    tmp['Scenario'] = s
    main_df = pd.concat([main_df, tmp])

main_df.rename(columns={'bus_label':'Balance',
                        'type':'Direction',
                        'obj_label':'Unit',
                        'datetime': 'Date'}, inplace=True)

# restore orginial df multiindex
main_df.set_index(['Scenario', 'Balance', 'Direction', 'Unit', 'Date'],
                   inplace=True)

# set colors
components = main_df.index.get_level_values('Unit').unique()
colors = dict(zip(components,
                  sns.color_palette("coolwarm_r", len(components))
                 )
            )

# select heat flows from main_df
idx = pd.IndexSlice
heat_df = main_df.loc[idx[scenarios, 'heat_balance', 'input', :, :]].unstack([0, 1, 2, 3])
heat_df.columns = heat_df.columns.droplevel([0, 2, 3])
heat_df.columns.name = 'Unit'