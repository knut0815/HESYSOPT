# -*- coding: utf-8 -*-
""" In this file additional groupings for new components are defined.

    oemof.solph uses so called grouping functions to group components for
    constraint creation. For new defined classes in `blocks.py` we
    add this grouping functionality here. We can not only group by new defined
    `blocks` but also add nodes to already existing solph `blocks`.
"""
import oemof.solph as solph
from oemof import groupings as grp
from nodes import (ExtractionTurbine, BackpressureTurbine,
                   ExtractionTurbineExtended, BackpressureTurbineExtended,
                   Boiler, ElectricalBus)
import blocks

# ############################ Grouping #######################################
def constraint_grouping(node):
    if isinstance(node, solph.Storage):
        return solph.blocks.Storage
    if (isinstance(node, ExtractionTurbine) and not
            isinstance(node, ExtractionTurbineExtended)):
        return blocks.ExtractionTurbine
    if isinstance(node, ExtractionTurbineExtended):
        return blocks.ExtractionTurbineExtended
    if (isinstance(node, BackpressureTurbine) and not
            isinstance(node, BackpressureTurbineExtended)):
        return blocks.BackpressureTurbine
    if isinstance(node, BackpressureTurbineExtended):
        return blocks.BackpressureTurbineExtended
    if isinstance(node, Boiler):
        return solph.blocks.LinearTransformer
    if (isinstance(node, solph.Bus) and node.balanced):
        return solph.blocks.Bus


def standard_flow_key(n):
    for f in n.outputs.values():
        if f.investment is None:
            return solph.blocks.Flow

def standard_flows(n):
    return [(n, t, f) for (t, f) in n.outputs.items()
            if f.investment is None]

def merge_standard_flows(n, group):
    group.extend(n)
    return group

standard_flow_grouping = grp.Grouping(
    key=standard_flow_key,
    value=standard_flows,
    merge=merge_standard_flows)

def discrete_flow_key(n):
    for f in n.outputs.values():
        if f.discrete is not None:
            return solph.blocks.Discrete

def discrete_flows(n):
    return [(n, t, f) for (t, f) in n.outputs.items()
            if f.discrete is not None]

def merge_discrete_flows(n, group):
    group.extend(n)
    return group

discrete_flow_grouping = grp.Grouping(
    key=discrete_flow_key,
    value=discrete_flows,
    merge=merge_discrete_flows)

GROUPINGS = [constraint_grouping, standard_flow_grouping,
             discrete_flow_grouping]

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