# -*- coding: utf-8 -*-
"""

"""
import os
from hesysopt.app import main

scenarios = ['base']

# configure app
arguments = {}
arguments['--scenario_name'] = scenarios[0]
arguments['--node_data'] = '../simple_example/nodes_flows.csv'
arguments['--sequence_data'] = '../simple_example/nodes_flows_seq.csv'
arguments['--start'] = '01/01/2014'
arguments['--end'] = '12/31/2014'
arguments['--freq'] = '1H'
arguments['--loglevel'] = 'INFO'
arguments['--solver-output'] = 'True'
arguments['--solver'] = 'gurobi'

# output directory
homepath = os.path.expanduser("~")
mainpath = os.path.join(homepath, 'hesysopt_simulation')
arguments['--output-directory'] =  mainpath


# run app
es, om, df = main(**arguments)