# -*- coding: utf-8 -*-
"""
"""
from hesysopt.plots.config import main_df, colors, plt, pd

main_df = main_df.loc['base']
chps = ['BP1', 'BP2']

fig, axes = plt.subplots(nrows=1, ncols=len(chps), figsize=(12,6))
i = 0
for c in chps:
    df_plot = pd.DataFrame()
    df_plot['P'] = main_df.loc['electrical_balance', 'to_bus', c].val
    df_plot['Q'] = main_df.loc['heat_balance', 'to_bus', c].val
    df_plot['H'] = main_df.loc['gas_balance', 'from_bus', c].val

    if c == 'EXT':
        eta_total = (main_df.loc['electrical_balance', 'to_bus', c].val +
            main_df.loc['heat_balance', 'to_bus', c].val) / main_df.loc['gas_balance', 'from_bus', c].val
        eta_el = (main_df.loc['electrical_balance', 'to_bus', c].val) / main_df.loc['gas_balance', 'from_bus', c].val
        eta_th = (main_df.loc['heat_balance', 'to_bus', c].val) / main_df.loc['gas_balance', 'from_bus', c].val

    df_plot.plot(ax=axes[i], kind='scatter', x='Q', y='P',
            title='PQ-Diagramm '+c, color=colors[c])
    i += 1

