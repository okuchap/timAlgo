import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import numpy as np


def Initialize_H(G):
    '''
    Initialize a matching M and prices of all vertices.

    Parameters
    ----------
    G = (V+W, E): a bipartite graph
        V+W: vertices
            price
        E: edges
            cost(nonnegative)
    M: a list of the edges which are a subset of E, a graph attribute

    Return
    ------
    H: initialized graph with zero prices and an empty matching M
    '''

    H = G.copy()

    # Initialize a matching
    # graph attributeとして定義
    H.graph['M_edges'] = []
    H.graph['M_vertices'] = []

    # Initialize prices
    for v in H.nodes():
        H.node[v]['price'] = 0

    return H


def BFS_GP(G, r, V, W):
    '''
    Implementing BFS modified for a good path

    Parameters
    ----------
    G=(V+W, E): a bipartite graph with a current matching M
        V+W: vertices
            p: prices
        M: a current matching
    r: the first unmatched vertex r of V(the root of a BFS tree)
    Return
    ------
    a list (path, S, N)
        path: a list of vertices representing a stucked path P, [r, ..., v]
        S: even level vertices of the BFS tree
        N: odd level ones
    '''

    def candidates(G, v, level):
        '''return a list of vertices(say, candidates) that satisfy the condition(*):
            1. adding (v,p) to the current path keep the path M-alternating
            2. (v,p) is tight
            3. p has not been reached before
        If the length of the returned list is zero, BFS is stucked.

        Paremeters
        ----------
        G: a bipartite graph
        v: a current node
        level: a current level of BFS(v lies in level i of the BFS tree)

        Return
        ------

        '''

        # Check if stucked or not
        # level: odd のとき(v is in W)は、matchingに含まれる枝の中から探す必要あり
        # level: even のとき(v is in V)は、まだ訪れていない(pastを使う)tight edgesから探す必要あり
        if level % 2 != 0:
            # このときcandidatesには多くとも一点しか（vとmatchしている点）含まれないはず
            candidates = [p for p in G.neighbors(
                v) if (p in G.graph['M_vertices'])]
        else:
            candidates = [p for p in G.neighbors(v) if ((not p in past) and (
                G[v][p]['cost'] - G.node[v]['price'] - G.node[p]['price'] == 0))]

        return candidates

    # 過去に訪れた点を格納するためのリスト
    past = []
    # これから訪れる点を格納するためのqueue
    future = deque()
    # pathを格納するためのリスト
    path = []
    # BFS treeを格納するためのlist, S: even level, N: odd level
    S = []
    N = []

    # set a distance from the root
    for p in G.nodes():
        if (p != r):
            G.node[p]['distance'] = float('inf')
        else:
            G.node[p]['distance'] = 0

    # set a current node v as r
    v = r
    # level of a BFS tree
    level = 0
    # candidates, a list of nodes
    candidates = candidates(G, v, level)

    while(len(candidates) != 0 and not (set(V) <= set(G.graph['M_vertices']))):
        # level = 0, or unstucked and there is a unmatched vertex of V
        # v: current vertex
        # level: current level
        past.append(v)
        if (level % 2 == 0):
            S.append(v)
        else:
            N.append(v)

        level += 1

        for p in candidates:
            if p not in future:
                future.append(p)
            G.node[p]['distance'] = G.node[v]['distance'] + 1

        v = future.popleft()
        candidates = candidates(G, v, level)

    # After terminating the while loop, BFS search is stucked
    # First, check if v is another unmatched vertex or not
    if (v in G.graph['M_vertices']):
        # v is a matched vertex
        return 'stuck'
    else:
        # v is unmatched
        # Construct a good path from r to v
        # 以下、sからeへのpathが存在する場合
        # 終点から遡ってpathを形成する
        pp = v
        while (1):
            path.insert(0, pp)
            if pp == r:
                break

            pred = G.predecessors(pp)

            for p in pred:
                if (G.node[p]['distance'] == G.node[pp]['distance'] - 1
                    and (G[p][pp]['cost'] - G.node[p]['price'] - G.node[pp]['price'] == 0)):
                    pp = p
                    break

        return [path, S, N]


def Hungarian(G, V, W):
    '''Solving min-cost bipartite matching problem

    Parameters
    ----------
    G=(V+W, E): a bipartite graph
        V+W: vertices, |V| = n
            prices
        E: edges
            cost>=0
            the reduced cost of (v,w) =  cost of (v,w) - price of v - price of w
        M: matching
    Invariants:
        1. the reduced costs of all edges in G >= 0
        2. the reduced costs of all edges in M = 0(tight)

    Return
    ------
    the min-cost matching M of G
    '''

    H = Initialize_H(G)

    while (len(H.graph['M_vertices']) != len(V)):
        # a current matching M is not a perfect matching

        # pick a unmatched node in V
        for p in V:
            if (p not in H.graph['M_vertices']):
                r = p
                break

        # S: even level vertices of the BFS tree
        # N: odd level ones
        # path: a stucked path
        path, S, N = BFS_GP(G, r, V, W)

        if (path[len(path) - 1] in (set(W) - set(H.graph['M_vertices']))):
            # the path contains an unmatched vertex w in W
            # If such w exists, it is the last vertex of the path
            # replace M
            for i in range(len(path) - 1):
                if (i % 2 == 0):
                    # the edge is from V to W, is not in M
                    if (not path[i] in H.graph['M_vertices']):
                        # 毎度条件をcheckするのは非効率的か
                        H.graph['M_vertices'].append(path[i])
                    # 両方向に枝を追加
                    H.graph['M_edges'].append((path[i], path[i + 1]))
                    H.graph['M_edges'].append((path[i + 1], path[i]))
                else:
                    # the edge is from W to V, is in M
                    if (not path[i] in H.graph['M_vertices']):
                        H.graph['M_vertices'].append(path[i])
                    H.graph['M_edges'].remove((path[i], path[i + 1]))
                    H.graph['M_edges'].remove((path[i + 1], path[i]))
        else:
            # set diff as the reduced cost of the last edge in the stucked path
            diff = G[path[len(path) - 2]][path[len(path) - 1]]['cost'] - \
                G.node[path[len(path) - 2]]['price'] - \
                G.node[len(path) - 1]['price']
            for v in S:
                G.node[v]['price'] += diff
            for w in N:
                G.node[w]['price'] -= diff

    return H.graph['M_edges']
