# -*- coding: utf-8 -*-
"""

"""
import os

costs = {'LOW': 55,
         'MED': 70,
         'HIGH': 95}

scenarios = {'1MWh_LOW-1H_2010': {},
             '2MWh_LOW-1H_2010': {},
             '3MWh_LOW-1H_2010': {},
             '4MWh_LOW-1H_2010': {},
             '5MWh_LOW-1H_2010': {},
             '1MWh_LOW-2H_2010': {},
             '2MWh_LOW-2H_2010': {},}


for s in scenarios.keys():
    paths = s.split('-')
    fcosts = paths[0].split('_')[1]
    freq = paths[1].split('_')[0]

    fuel_costs = costs[fcosts]
    nominal_capacity = int(paths[0].split('_')[0].strip('MWh'))
    node_path = os.path.join('data/', paths[0]+'.csv')
    seq_path = os.path.join('data/', paths[1]+'_seq.csv')

    # assign extracted values
    scenarios[s]['freq'] = freq
    scenarios[s]['node_path'] = node_path
    scenarios[s]['seq_path'] = seq_path
    scenarios[s]['fuel_costs'] = fuel_costs
    scenarios[s]['nominal_capacity'] = nominal_capacity


