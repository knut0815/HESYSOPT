# -*- coding: utf-8 -*-
"""

"""
############################# imports #########################################
# python package imports
import pandas as pd

# oemof imports
from oemof.core import energy_system as oces
from oemof.solph import Flow, OperationalModel, Sink
from oemof.solph.options import Discrete

# heat system optimizatio import
from hesysoptim.nodes import (ExtractionTurbine, BackpressureTurbine, Boiler,
                              HeatBus, ElectricalBus, ResourceBus)
import hesysoptim.blocks as blocks
from hesysoptim.helpers import GROUPINGS

# ############################### EnergySystem ################################
heating_system = oces.EnergySystem(groupings=GROUPINGS)


# ################################# Buses #####################################
boil = ResourceBus(label='boil', balanced=False)
bgas = ResourceBus(label="bgas", balanced=False)
belec = ElectricalBus(label="electricity", balanced=False)
bheat = HeatBus(label="heat")

# ############################## Components ###################################
## Demand (sink)
dem = Sink(label="demand", inputs={bheat: Flow(nominal_value=15,
                                               actual_value=0.7,
                                               fixed=True)})

## Simple Boiler
boi = Boiler(label='boi',
             inputs={boil: Flow(nominal_value=20,
                                variable_costs=10)},
             outputs = {bheat: Flow()},
             conversion_factors={bheat: 0.9})

##  Extraction turbine
extr = ExtractionTurbine(label="extr",
                        inputs={bgas: Flow(nominal_value=20,
                                           variable_costs=10)},
                        outputs={belec: Flow(nominal_value=10,
                                             variable_costs=-5, min=0.5,
                                             discrete=Discrete()),
                                 bheat: Flow()},
                        power_loss_index=0.12,
                        power_heat_index=0.7,
                        efficiency_condensing=0.4)

## Backpressure Turbine
backpr = BackpressureTurbine(label="backpr",
                             inputs={bgas: Flow(nominal_value=20,
                                                variable_costs=10)},
                             outputs={belec: Flow(nominal_value=10,
                                                  variable_costs=-5, min=0.5,
                                                  discrete=Discrete()),
                                      bheat: Flow()},
                             conversion_factors={belec: 0.4,
                                                 bheat: 0.5}
                             )

# ########################## Optimization Model ###############################
datetime_index = pd.date_range('1/1/2016', periods=3, freq='60min')
om = OperationalModel(es=heating_system, timeindex=datetime_index,
                      constraint_groups=[blocks.ExtractionTurbine])

om.solve(solve_kwargs={'tee':True})
om.write('district_heating_optimization.lp',
         io_options={'symbolic_solver_labels':True})
