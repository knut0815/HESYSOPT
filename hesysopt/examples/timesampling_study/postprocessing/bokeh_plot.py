# -*- coding: utf-8 -*-
"""

"""
from bokeh.charts import Area, show, vplot, output_file, defaults, Step
from hesysopt.plots.config import heat_df, colors, pd
from bokeh.palettes import brewer

palette = brewer["Blues"][3]
heat_df.columns = heat_df.columns.swaplevel(0,1)

df = heat_df['BP1']
df.index = df.index.droplevel([0,1])
# filling for
df.fillna(method='ffill', inplace=True)


defaults.width = 1000
defaults.height = 400

dct = {c: df[c].values for c in df if c !='STO'}
area2 = Step(dct,
             title="Heat Production", legend="top_left", xlabel='Date',
             ylabel='Heat in MWh', palette=palette)

output_file("area.html", title="HESYSOPT Results")
show(area2)