# -*- coding: utf-8 -*-
from hesysopt.plots.config import heat_df, colors, pd

df = heat_df['4HBP']
# filling for
df.fillna(method='ffill', inplace=True)
dct = {c: df.sort_values(by=c, ascending=False)[c].values for c in df}
df_sorted = pd.DataFrame(dct, columns=df.columns)
axes = df_sorted.plot(lw=2, title='Sorted heat curves',
                      colors=list(map(colors.get, df.columns)))
axes.set_xlabel('Hours')
axes.set_ylabel('Heat in MW')


#fig1 = plt.figure(1)
#fig1 = df.sum().plot(kind="bar", color=list(map(colors.get, df.columns)))

#
from bokeh.charts import show, output_file, Step
heat_df.columns = heat_df.columns.swaplevel(0,1)

df = heat_df['BP1']
df.index = df.index.droplevel([0,1])
# filling for
df.fillna(method='ffill', inplace=True)


dct = {c: df.sort_values(by=c, ascending=False)[c].values for c in df}
area2 = Step(dct,
             title="Heat Production", legend="top_left", xlabel='Date',
             ylabel='Heat in MWh')

output_file("area.html", title="HESYSOPT Results")
show(area2)