# -*- coding: utf-8 -*-
"""

"""
############################# imports #########################################
# python package imports
import pandas as pd

from oemof.solph import (Flow, OperationalModel, Bus, Sink, EnergySystem,
                         BinaryFlow)
from oemof.outputlib import ResultsDataFrame
# heat system optimizatio import
from hesysopt.nodes import ExtractionTurbine, BackpressureTurbine, Boiler
from hesysopt.helpers import GROUPINGS, ADD_SOLPH_BLOCKS

# ############################### EnergySystem ################################
# see pandas date_range documentation for details
datetime_index = pd.date_range('1/1/2016', periods=24, freq='1H')

heating_system = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)


# ################################# Buses #####################################
boil = Bus(label='boil', balanced=False)
bgas = Bus(label="bgas", balanced=False)
belec = Bus(label="electrical_balance", balanced=False)
bheat = Bus(label="heat_balance")

# ############################## Components ###################################
# Demand (sink) Note: for this sink there is a constant, fixed demand
#                     of 15*0.5=7.5, you may provide an array for actual
#                     value, to get a timedepent demand
dem = Sink(label="demand", inputs={bheat: Flow(nominal_value=15,
                                               actual_value=0.5,
                                               fixed=True)})

## Simple Boiler
boi = Boiler(label='BOI',
             inputs={boil: Flow(nominal_value=20,
                                variable_costs=10)},
             outputs = {bheat: Flow()},
             conversion_factors={bheat: 0.9})

##  Extraction turbine (simple)
# Note: The values for efficiency_condesing, power_loss_index and
#       conversion_factors, need to be compatible with each other to get
#       a correct model
extr = ExtractionTurbine(label="EXT", conversion_factors={belec: 0.514,
                                                          bheat: 0.3},
                        inputs={bgas: Flow(nominal_value=20,
                                           variable_costs=10)},
                        outputs={belec: Flow(nominal_value=10,
                                             variable_costs=-5, min=0.5,
                                             discrete=BinaryFlow()),
                                 bheat: Flow()},
                        power_loss_index=0.12,
                        efficiency_condensing=0.55)

## Backpressure Turbine (simple)
backpr = BackpressureTurbine(label="BP",
                             inputs={bgas: Flow(nominal_value=20,
                                                variable_costs=10)},
                             outputs={belec: Flow(nominal_value=10,
                                                  variable_costs=-5, min=0.5,
                                                  discrete=BinaryFlow()),
                                      bheat: Flow()},
                             conversion_factors={belec: 0.4,
                                                 bheat: 0.5}
                             )

# ########################## Optimization Model ###############################
# create optimzation odel
# this is basically a pyomo ConcreteModel with additional elements from oemof
om = OperationalModel(es=heating_system, constraint_groups=ADD_SOLPH_BLOCKS)
# solve the model (thats NOT a solve mehtod, but a method of
#                  oemof.solph.OperationalModel)
om.solve(solver='gurobi', solve_kwargs={'tee':True})

# create standard oemof multiindex results dataframe
df = ResultsDataFrame(energy_system=heating_system)

idx = pd.IndexSlice
# This will give the heat input into the heat balance from all units
heat_df = df.loc[idx['heat_balance', 'to_bus', :, :]].unstack([0, 1, 2])
heat_df.columns = heat_df.columns.droplevel([0, 1, 2])
print(heat_df.head(20))

# write lp file
#om.write('district_heating_optimization.lp',
#         io_options={'symbolic_solver_labels':True})
