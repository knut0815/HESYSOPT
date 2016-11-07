# -*- coding: utf-8 -*-
"""

"""
import os
import pandas as pd
from oemof.solph.inputlib import csv_tools as tools


base_nodes_df = pd.read_csv('data/basefile_BP.csv', index_col=[0,1,2,3])
base_seq_df = pd.read_csv('data/basefile_BP_seq.csv', header=[0,1,2,3,4])

# fuel costs for gas
costs = {'LOW': 55,
         'MED': 70,
         'HIGH': 95}
# scenario names
scenarios = {'1MWh_LOW-1H_2010-BP': {},
             '2MWh_LOW-1H_2010-BP': {},
             '3MWh_LOW-1H_2010-BP': {},
             '4MWh_LOW-1H_2010-BP': {},
             '5MWh_LOW-1H_2010-BP': {},
             '1MWh_LOW-2H_2010-BP': {},
             '2MWh_LOW-2H_2010-BP': {},}

for s in scenarios.keys():
    paths = s.split('-')
    freq = paths[1].split('_')[0]
    year = paths[1].split('_')[1]
    fuel_costs_key = paths[0].split('_')[1]
    nominal_capacity = int(paths[0].split('_')[0].strip('MWh'))
    fuel_costs = costs[fuel_costs_key]
    node_path = os.path.join('data/', paths[0]+'.csv')
    seq_path = os.path.join('data/', paths[1]+'_seq.csv')

    # alter base - pandas df
    base_nodes_df.ix[('Source', 'GAS', 'GAS', 'gas_balance'),
                'variable_costs'] = fuel_costs
    base_nodes_df.ix[('Storage', 'STO', 'STO', 'heat_balance'),
                'nominal_capacity'] = nominal_capacity

    tools.resample_sequence(seq_base_file='data/basefile_BP_seq.csv',
                            output_path='data/sequences',
                            file_prefix=str(year)+'_',
                            file_suffix='_',
                            samples=[freq],
                            header=[0,1,2,3,4])

    # assign extracted values
    scenarios[s]['freq'] = freq
    scenarios[s]['node_path'] = node_path
    scenarios[s]['seq_path'] = seq_path
    #scenarios[s]['fuel_costs'] = fuel_costs
    #scenarios[s]['nominal_capacity'] = nominal_capacity

    base_nodes_df.to_csv(node_path)


