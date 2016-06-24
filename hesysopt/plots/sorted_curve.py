# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


path = './data/results.csv'
main_df = pd.read_csv(path)
# restore orginial df multiindex
main_df.set_index(['bus_label', 'type', 'obj_label', 'datetime'], inplace=True)

idx = pd.IndexSlice
df = main_df.loc[idx['heat_balance',
                     'input',
                     ['extr_turbine_ext', 'bp_turbine', 'oil_boiler'],
                     :]].unstack([0,1,2])

df.columns = df.columns.droplevel([0, 1, 2])
df.columns.name = 'Unit'

dct = {c: df.sort_values(by=c, ascending=False)[c].values for c in df}
df_sorted = pd.DataFrame(dct, columns=df.columns)
axes = df_sorted.plot(lw=2, title='Sorted heat curves')
axes.set_xlabel('Hours')
axes.set_ylabel('Heat in MW')





