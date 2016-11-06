# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
from hesysopt.restore_results import restore

main_df, scenarios, colors = restore(['1HBP'])

idx = pd.IndexSlice
heat_df = main_df.loc[idx[scenarios,
                          'heat_balance',
                          'to_bus', :, :]].unstack(['Scenario', 'obj_label'])
heat_df.columns = heat_df.columns.droplevel([0])
heat_df.columns.name = 'Unit'

el_df = main_df.loc[idx[scenarios,
                        'electrical_balance',
                        'to_bus', :, :]].unstack(['Scenario', 'obj_label'])


