# dequeをimport
from collections import deque


def BFS(G, s):
    '''
    Implementing BFS

    Parameters
    ----------
    G=(V, E): a graph
        V's attribute
            v.color, v.parent, v.distance
    s: a starting point

    Return
    ------
    None
    '''

    # 全ての頂点を初期化
    for v in G.nodes():
        G.node[v]['color'] = 'white'
    for v in G.nodes():
        G.node[v]['distance'] = float('inf')
    for v in G.nodes():
        G.node[v]['parent'] = None

    # sについて初期化
    G.node[s]['color'] = 'gray'
    G.node[s]['distance'] = 0

    queue = deque()
    queue.append(s)

    while len(queue) > 0:
        u = queue.popleft()
        for v in G.successors(u):
            if (G.node[v]['color'] == 'white'):
                G.node[v]['color'] == 'gray'
                G.node[v]['distance'] == G.node[u]['distance'] + 1
                G.node[v]['parent'] = u
                queue.append(v)
        G.node[v]['color'] = 'black'

def BFS_path(G, s, t):
    '''
    Implementing BFS

    Parameters
    ----------
    G=(V, E): a graph
        V's attribute
            v.color, v.parent, v.distance
    s: a starting point
    t: an end point

    Return
    ------
    a shortest path from s to t
    '''

    BFS(G, s)
    path = []
    v = t
    if (G.node[v]['distance'] == float('inf')):
        print('there is no path')
        return []

    while (v != s):
        path.insert(0, v)
        v = G.node[v]['parent']
    path.insert(0, v)
    return path