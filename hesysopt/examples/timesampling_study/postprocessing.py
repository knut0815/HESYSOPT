# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import seaborn as sns

def sorted_curves(df, colors):
    df.fillna(method='ffill', inplace=True)
    dct = {c: df.sort_values(by=c, ascending=False)[c].values for c in df}
    df_sorted = pd.DataFrame(dct, columns=df.columns)
    ax = df_sorted.plot(lw=2, title='Sorted heat curves',
                          color=list(map(colors.get, df.columns)))
    ax.set_xlabel('Hours')
    ax.set_ylabel('Output in MW')
    return ax

def summed_production(df, colors):
    df.fillna(method='ffill', inplace=True)
    summed = df.sum() * 1e-3 # to GWh
    ax = summed.plot(kind='bar', title="Total heat production by Unit",
                     color=list(map(colors.get, df.columns)))
    ax.set_ylabel("Output in GWh")
    ax.set_xlabel("Unit")
    return ax

def seaborn_summed_production(df, colors):
    # factor plot with seabor for multiple scenarios
    sns.set(style='ticks')
    summed = df.sum().reset_index()
    fg = sns.factorplot(x='Unit',
                            y=0, col='Scenario', data=summed, kind='bar',
                            palette=list(map(colors.get, df.columns)))
                            # hue='Scenario'
    fg.set_ylabels('Heat in GWh')

def compare_objectives(df, colors):
    x = pd.concat([df,
                   df['scenario_name'].apply(lambda df:
                                             pd.Series(df.split('_')))], axis=1)
    x.rename(columns={0: 'storage', 1: 'year', 2: 'sample'}, inplace=True)

    g = sns.factorplot(y="objective", x='storage', #hue='storage',
                       col="sample", col_wrap=2,
                       data=x,
                       kind="bar", size=2.5, aspect=.8)
    return x
#from bokeh.charts import Area, show, vplot, output_file, defaults, Step
#from hesysopt.plots.config import heat_df, colors, pd
#from bokeh.palettes import brewer
#
#palette = brewer["Blues"][3]
#heat_df.columns = heat_df.columns.swaplevel(0,1)
#
#df = heat_df['BP1']
#df.index = df.index.droplevel([0,1])
## filling for
#df.fillna(method='ffill', inplace=True)
#
#
#defaults.width = 1000
#defaults.height = 400
#
#dct = {c: df[c].values for c in df if c !='STO'}
#area2 = Step(dct,
#             title="Heat Production", legend="top_left", xlabel='Date',
#             ylabel='Heat in MWh', palette=palette)
#
#output_file("area.html", title="HESYSOPT Results")
#show(area2)