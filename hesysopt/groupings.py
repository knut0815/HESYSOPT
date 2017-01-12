# -*- coding: utf-8 -*-
""" In this file additional groupings for new components are defined.

    oemof.solph uses so called grouping functions to group components for
    constraint creation. For new defined classes in `blocks.py` we
    add this grouping functionality here. We can not only group by new defined
    `blocks` but also add nodes to already existing solph `blocks`.
"""
import oemof.solph as solph
from oemof import groupings
from hesysopt.nodes import (ExtractionTurbine, BackpressureTurbine,
                   ExtractionTurbineExtended, BackpressureTurbineExtended,
                   Boiler, ElectricalBus)
import hesysopt.blocks as blocks

# ############################ Grouping #######################################
def constraint_grouping(node):
    if (isinstance(node, solph.Storage) and
        isinstance(node.investment, solph.Investment)):
        return solph.blocks.InvestmentStorage
    if isinstance(node, solph.Storage):
        return solph.blocks.Storage
        return solph.blocks.Storage
    if type(node) == ExtractionTurbine:
        return blocks.ExtractionTurbine
    if type(node) == ExtractionTurbineExtended:
        return blocks.ExtractionTurbineExtended
    if  type(node) == BackpressureTurbine:
        return blocks.BackpressureTurbine
    if type(node) == BackpressureTurbineExtended:
        return blocks.BackpressureTurbineExtended
    if type(node) == Boiler:
        return solph.blocks.LinearTransformer
    if type(node) == solph.Bus and node.balanced:
        return solph.blocks.Bus


investment_flow_grouping = groupings.FlowsWithNodes(
    constant_key=solph.blocks.InvestmentFlow,
    # stf: a tuple consisting of (source, target, flow), so stf[2] is the flow.
    filter=lambda stf: stf[2].investment is not None)

standard_flow_grouping = groupings.FlowsWithNodes(
    constant_key=solph.blocks.Flow)

binary_flow_grouping = groupings.FlowsWithNodes(
    constant_key=solph.blocks.BinaryFlow,
    filter=lambda stf: stf[2].binary is not None)

discrete_flow_grouping = groupings.FlowsWithNodes(
    constant_key=solph.blocks.DiscreteFlow,
    filter=lambda stf: stf[2].discrete is not None)

GROUPINGS = [constraint_grouping, standard_flow_grouping,
             binary_flow_grouping, discrete_flow_grouping,
             investment_flow_grouping]

# ####################### classes dict for csv-reader #########################

ADD_SOLPH_BLOCKS = [blocks.BackpressureTurbine, blocks.ExtractionTurbine,
                    blocks.ExtractionTurbineExtended,
                    blocks.BackpressureTurbineExtended]

ADD_CSV_CLASSES = {'ExtractionTurbine': ExtractionTurbine,
                   'BackpressureTurbine': BackpressureTurbine,
                   'ExtractionTurbineExtended': ExtractionTurbineExtended,
                   'BackpressureTurbineExtended': BackpressureTurbineExtended,
                   'Boiler': Boiler,
                   'ElectricalBus': ElectricalBus}

ADD_CSV_SEQ_ATTRIBUTES = ['power_loss_index']

ADD_FLOW_ATTRIBUTES = ['linked', 'linked_nominal_value']
