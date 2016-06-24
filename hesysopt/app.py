# -*- coding: utf-8 -*-
''' HESYSOPT v0.0.1

Usage: app.py [options]

Options:
      --start=START             Start of the simulation.
                                [default: 1/1/2014]
      --end=END                 End of the simulation.
                                [default: 02/01/2014]
      --node_data=NODE_DATA     CSV-file with data for nodes and associated flows.
                                [default: ./data/nodes_flows.csv]
      --sequence_data=SEQ_DATA  CSV-file with sequence data for flows/nodes.
                                [default: ./data/nodes_flows_seq.csv]
      --name=NAME               Name of the model.
                                [default: HESYSModel]
      --solver=SOLVER           Solver to use to for optimization problem
                                [default: glpk]
      --solver-output           Print the solver-output on console.
                                [default: False]
      --output-directory        Directory where results, logs etc are stored.
                                Default is the home path of the system.
  -l, --loglevel=LOGLEVEL       Set the loglevel. Should be one of DEBUG, INFO,
                                WARNING, ERROR or CRITICAL. [default: INFO]
  -h, --help                    Display this help.
  -v, --version                 Display version information.
'''

# python package imports
try:
  from docopt import docopt
except ImportError:
  print("Unable to import docopt.\nIs the 'docopt' package installed?")
import pandas as pd
import logging
import os
import time

from oemof.tools import logger
from oemof.outputlib import ResultsDataFrame
from oemof.solph import OperationalModel, EnergySystem, NodesFromCSV

# heat system optimizatio import
from helpers import (GROUPINGS, ADD_CSV_CLASSES, ADD_CSV_SEQ_ATTRIBUTES,
                     ADD_SOLPH_BLOCKS)

logger.define_logging()

# ########################## Functions ########################################
def create_nodes(**arguments):
    """Creates nodes from provided csv-files.
    """
    node_data = arguments['--node_data']
    sequence_data = arguments['--sequence_data']

    logging.info("Reading nodes from csv-files...")
    nodes = NodesFromCSV(file_nodes_flows=node_data,
                         file_nodes_flows_sequences=sequence_data,
                         delimiter=',',
                         additional_classes=ADD_CSV_CLASSES,
                         additional_seq_attributes=ADD_CSV_SEQ_ATTRIBUTES)
    return nodes

def create_energysystem(nodes, **arguments):
    """Create the energysystem.
    """
    datetime_index = pd.date_range(start=arguments['--start'],
                                   end=arguments['--end'], freq='60min')
    es = EnergySystem(entities=nodes, time_idx=datetime_index,
                      groupings=GROUPINGS)
    es.timestamp = time.strftime("%Y%m%d-%H:%M:%S")

    return es

def simulate(es=None, **arguments):
    """Creates the optimization model, solves it and writes back results to
    energy system object

    Parameters
    ----------
    es : :class:`oemof.solph.network.EnergySystem` object
       Energy system holding nodes, grouping functions and other important
       information.
    **arguments : key word arguments
        Arguments passed from command line
    """


    logging.info("Creating optimization model...")
    om = OperationalModel(name=arguments['--name'],
                          es=es, constraint_groups=ADD_SOLPH_BLOCKS)

    if arguments['--loglevel'] == 'DEBUG':
        lppath = os.path.join(arguments['--output-directory'], "lp-files")
        if not os.path.exists(lppath):
            os.mkdir(lppath)
        lpfilepath = os.path.join(lppath, ''.join([om.name,
                                                   '_', es.timestamp, '.lp']))
        logging.info("Writing lp-file to '{}'".format(lpfilepath))
        om.write(lpfilepath, io_options={'symbolic_solver_labels':True})

    logging.info('Solving optimization model...')

    om.solve(arguments['--solver'],
             solve_kwargs={'tee':arguments['--solver-output']})

    om.results()

    return om

def write_results(es, om, **arguments):
    """Writes results to csv file
    """
    resultspath = os.path.join(arguments['--output-directory'],
                               'results' + es.timestamp)
    if not os.path.exists(resultspath):
        os.mkdir(resultspath)

    # use results dataframe for result writing
    df = ResultsDataFrame(energy_system=es)
    df.to_csv(os.path.join(resultspath, 'results.csv'))

    buses = df.index.get_level_values('bus_label').unique()
    for b in buses:
        df_out = df.slice_by(bus_label=b).unstack([0,1,2])
        df_out.to_csv(os.path.join(resultspath, ''.join([b, '.csv'])))

    return df


def main_path(**arguments):
    """Sets the main path for the simulation results, lpfiles etc.
    """
    if not arguments['--output-directory']:
        homepath = os.path.expanduser("~")
        mainpath = os.path.join(homepath, 'hesysopt_simulation')

        if not os.path.exists(mainpath):
            os.mkdir(mainpath)

    return mainpath

def main(**arguments):
    """
    """
    logging.info("Starting HEYSYSOPT!")

    arguments['--output-directory'] = main_path(**arguments)

    logging.getLogger().setLevel(getattr(logging, arguments['--loglevel']))
    if arguments['--loglevel'] == 'DEBUG':
        print(arguments)
    # create nodes from csv
    nodes = create_nodes(**arguments)
    # create energy system and pass nodes
    es = create_energysystem(nodes=[n for n in nodes.values()], **arguments)
    # create optimization model and solve it and write results back to energys
    om = simulate(es=es, **arguments)
    # write results to csv file
    results_df = write_results(es=es, om=om, **arguments)

    logging.info("Done!")

    return es, om, results_df


############################## main ###########################################
if __name__ == '__main__':
    arguments = docopt(__doc__, version='HESYSOPT v0.0.1')
    #arguments['--node_data'] = 'data/casestudy/nodes_flows_base.csv'
    #arguments['--sequence'] = 'data/casestudy/nodes_flows_seq_base.csv'
    arguments['--start'] = '01/01/012'
    arguments['--end'] = '06/01/2012'
    arguments['--loglevel'] = 'DEBUG'
    es, om, df = main(**arguments)






