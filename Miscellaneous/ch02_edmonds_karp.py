"""
Edmonds-Karp algorithm for maximum flow problems.
"""

import networkx as nx
from networkx.algorithms.flow.utils import *
def edmonds_karp_core(R, s, t, cutoff):
    R_node = R.node
    R_pred = R.pred
    R_succ = R.succ

    #inf = R.graph['inf']

    def augment(path):
        '''
        augment flow along a path from s to t.
        path is a list of nodes.
        '''

        # Determine the path residual capacity
        flow = float('inf')
        it = iter(path)
        u = next(it)
        for v in it:
            attr = R_succ[u][v]
            flow = min(flow, attr['capacity'] - attr['flow'])
            u = v

        # Augment flow along the path
        it = iter(path)
        u = next(it)
        for v in it:
            R_succ[u][v]['flow'] += flow
            R_succ[v][u]['flow'] -= flow
            u = v
        
        return flow