# -*- coding: utf-8 -*-
"""

"""
from hesysopt.plots.config import heat_df, colors
import seaborn


# drop unwanted components
heat_df.drop(['STO'], level=1, inplace=True, axis=1)


# plot
s = 'base'
summed = heat_df[s].sum() * 1e-3 # to GWh
ax = summed.plot(kind='bar', title="Total heat production by Unit",
                 colors=list(map(colors.get, heat_df[s].columns)))
ax.set_ylabel("Heat in GWh")
ax.set_xlabel("Unit")

# factor plot with seabor for multiple scenarios
seaborn.set(style='ticks')
summed = heat_df.sum().reset_index()
fg = seaborn.factorplot(x='Unit',
                        y=0, col='Scenario', data=summed, kind='bar',
                        palette=list(map(colors.get, heat_df[s].columns)))
                        # hue='Scenario'
fg.set_ylabels('Heat in GWh')

import pandas as pd
heat_df.index = pd.date_range(start='2011', freq='1H', periods=8737)
ax = heat_df[s].resample('1D', how='sum').plot(kind='area',
                      colors=list(map(colors.get, heat_df[s].columns)))
ax.set_ylabel('Heat in MWh')
ax.set_xlabel('Hour of the year')