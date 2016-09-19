# -*- coding: utf-8 -*-
from hesysopt.plots.config import heat_df, colors, pd

df = heat_df['base']

dct = {c: df.sort_values(by=c, ascending=False)[c].values for c in df}
df_sorted = pd.DataFrame(dct, columns=df.columns)
axes = df_sorted.plot(lw=2, title='Sorted heat curves',
                      colors=list(map(colors.get, df.columns)))
axes.set_xlabel('Hours')
axes.set_ylabel('Heat in MW')


#fig1 = plt.figure(1)
#fig1 = df.sum().plot(kind="bar", color=list(map(colors.get, df.columns)))

