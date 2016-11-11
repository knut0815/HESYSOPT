# -*- coding: utf-8 -*-
"""

"""
import os
import numpy as np
import pandas as pd
from oemof.solph.inputlib import csv_tools as tools
import functions as func

spec_invest =  np.array([[35, 50,  100, 240, 260, 340,  380, 440, 590, 700],
                         [2000, 1500, 1250, 1054, 988, 950, 873, 759, 696, 543]])

#popt = func.investment_fit(spec_invest=spec_invest, plot=True)

def storage_invest_costs(U=1, size='small'):
    """
    U : float
     Energy amount in MWh
    """
    coeff = func.investment_fit(size=size)
    # calc volume
    V = func.storage_energy2volume(U=U*1e3)
    # calc spec. investment
    I = coeff[0] * V**coeff[1]
    I_total = I * V
    return I_total
x = storage_invest_costs()

def annual_costs(I=None, n=20, wacc=0.07):
    """ Calculate annual periodical costs from absolute investment I
    """
    annual_costs = I* (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)
    return annual_costs

base_nodes_df = pd.read_csv('data/basefile_BP.csv', index_col=[0,1,2,3])
base_seq_df = pd.read_csv('data/basefile_BP_seq.csv', header=[0,1,2,3,4])

# fuel costs for gas
costs = {'LOW': 55,
         'MED': 70,
         'HIGH': 95}
# scenario names
scenarios = {'1MWh_LOW-1H_2010-BP': {},
             '2MWh_LOW-1H_2010-BP': {},
             '4MWh_LOW-1H_2010-BP': {},
             '10MWh_LOW-1H_2010-BP': {},
             '14MWh_LOW-1H_2010-BP': {},
             '17MWh_LOW-2H_2010-BP': {}}

for s in scenarios.keys():
    paths = s.split('-')
    freq = paths[1].split('_')[0]
    year = paths[1].split('_')[1]
    fuel_costs_key = paths[0].split('_')[1]
    nominal_capacity = int(paths[0].split('_')[0].strip('MWh'))
    fuel_costs = costs[fuel_costs_key]
    node_path = os.path.join('data/', paths[0]+'.csv')
    seq_path = os.path.join('data/sequences', paths[1]+'_seq.csv')

    # alter base - pandas df
    base_nodes_df.ix[('Source', 'GAS', 'GAS', 'gas_balance'),
                'variable_costs'] = fuel_costs
    base_nodes_df.ix[('Storage', 'STO', 'STO', 'heat_balance'),
                'nominal_capacity'] = nominal_capacity
    base_nodes_df.ix[('Storage', 'STO', 'STO', 'heat_balance'),
                'fixed_costs'] = annual_costs(
                    I=storage_invest_costs(nominal_capacity))/nominal_capacity
    tools.resample_sequence(seq_base_file='data/basefile_BP_seq.csv',
                            output_path='data/sequences',
                            file_prefix=str(year)+'_',
                            file_suffix='',
                            samples=[freq],
                            header=[0,1,2,3,4])

    # assign extracted values
    scenarios[s]['freq'] = freq
    scenarios[s]['node_path'] = node_path
    scenarios[s]['seq_path'] = seq_path
    #scenarios[s]['fuel_costs'] = fuel_costs
    #scenarios[s]['nominal_capacity'] = nominal_capacity

    base_nodes_df.to_csv(node_path)

