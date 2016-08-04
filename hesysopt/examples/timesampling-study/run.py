# -*- coding: utf-8 -*-
"""

"""
import os
from hesysopt.app import main

scenarios = ['111-2014-LOW']

# configure app
arguments = {}
arguments['--scenario_name'] = scenarios[0]
arguments['--node_data'] = 'data/nodes_flows_'+scenarios[0]+'.csv'
arguments['--sequence_data'] = 'data/nodes_flows_seq_'+scenarios[0]+'.csv'
arguments['--start'] = '01/01/2014'
arguments['--end'] = '01/31/2014'
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