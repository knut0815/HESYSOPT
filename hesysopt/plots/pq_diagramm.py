# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:49:26 2016

@author: simon
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


path = './data/results.csv'
main_df = pd.read_csv(path)
# restore orginial df multiindex
main_df.set_index(['bus_label', 'type', 'obj_label', 'datetime'], inplace=True)

chps = ['extr_turbine_ext', 'bp_turbine']

fig, axes = plt.subplots(nrows=1, ncols=len(chps), figsize=(12,6))
i = 0
for c in chps:
    df_plot = pd.DataFrame()
    df_plot['P'] = main_df.loc['electrical_balance', 'input', c].val
    df_plot['Q'] = main_df.loc['heat_balance', 'input', c].val

    df_plot.plot(ax=axes[i], kind='scatter', x='Q', y='P',
            title='PQ-Diagramm '+c)
    i += 1
