# -*- coding: utf-8 -*-

import graphviz as gv
import oemof.network as ntwk


def plot_graph(es, filename=None):
    """
    """
    G = gv.Digraph(format='svg')
    for n in es.nodes:
        if isinstance(n, ntwk.Component):
            color='black'
            shape = 'box'
        else:
            color = 'blue'
            shape = None
        if 'heat' in n.label:
            color = 'red'
        if 'GL' in n.label:
            color='brown'
        if '_el' in n.label:
            color='blue'
        G.node(n.label, color=color, shape=shape)
    # add edges
    for s,t in es.om.flows:
        G.edge(s.label, t.label)
    G.render('G')

