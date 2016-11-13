def bfsFlowPath_(G, s, e):
    '''
    Inputs:
        G: a residual graph
        s: a start point
        e: an end point
        each edge has two attributes:
            capacity: (residual) capacity
            flow: (pre)flow <= capacity
    Output:
        path: a list of edges which represents a path from s to e.
        At each node of the path, its current flow is strictly less than its capacity.(residual capacity > 0)
        In case there is no path from s to t, return None.
    '''

    past = [s] # 過去に訪れた点を記録, sは最初から含んでおく
    path = []

    # 全ての点のsからの距離の初期値を無限大に
    for p in G.nodes():
        G.node[p]['dist'] = float('inf')
    
    # node s の距離を0に
    G.node[s]['dist'] = 0
    
    # sに隣接する点をqueueに
    # queueには、今後訪れるべき点が格納される
    queue = deque()
    for p in G.successors(s):
        # current flow < capacity となる(i.e. residual capacity > 0)edgeだけをpathの候補に
        # flow < capacity となるedge以外は存在しないものとして扱うのと同じ
        if G[s][p]['capacity'] > 0:
            queue.append(p)
            
    # あとで条件分岐に用いる
    numberOfSuccessorsOfSource = len(queue)
    
    # sに隣接する点の距離を1に
    for p in queue:
        G.node[p]['dist'] = 1

    # BFSを用いてresidual capacity > 0を満たすsからeへのpathがあるのか調べる
    # pastに過去に訪れた点を格納
    while len(queue)>0:
        v = queue.popleft()
        if v == e: break
        else:
            past.append(v)
            for p in G.successors(v):
                # (過去に訪れていない and residual capacity > 0 and 終点がsでない)を満たすedge
                if ( (not p in past) and ( G[v][p]['capacity'] > 0 )):
                    if ( not p in queue):
                        queue.append(p)
                    if G.node[p]['dist'] > G.node[v]['dist'] + 1:
                        G.node[p]['dist'] = G.node[v]['dist'] + 1

    # sからeへのpathが存在しない場合はNoneを返す
    if numberOfSuccessorsOfSource == 0:
        v = s
    if v != e or v == s:
        # print ('There is no path.')
        return None
    
    # 以下、sからeへのpathが存在する場合
    # 終点から遡ってpathを形成する
    pp = e
    while (1):
        if pp == s: break
            
        pred = G.predecessors(pp)
        
        count = 0

        for p in pred:
            # ここに、flow < capacity の条件を追加
            # distの作り方から、flow < capacityは自然に満たされる
            if ( G.node[p]['dist'] == G.node[pp]['dist']-1):
                path.insert(0, (p,pp))
                pp = p
                break
            else:
                count += 1
        
        # 条件を満たすedgeがない
        if count == len(pred):
            break
    
    # pathがない場合
    # 無駄な条件か？（ここまで来ているのなら、pathはあるはず。念のため残しておく。）
    if path[0][0] != s:
        return None
    
    return path

def makeResidualGraph(G):
    '''
    Input: a graph G
    Output: its residual graph Gf
    '''
    Gf = G.copy()
    edgeList = G.edges()
    
    # 逆向きのedgeがないものは追加
    for edge in edgeList:
        if not (edge[1], edge[0]) in edgeList:
            Gf.add_edge(edge[1],edge[0])
            Gf[edge[1]][edge[0]]['capacity'] = Gf[edge[0]][edge[1]]['flow']
            Gf[edge[1]][edge[0]]['flow'] = 0
    
    for edge in edgeList:
        Gf[edge[0]][edge[1]]['capacity'] = Gf[edge[0]][edge[1]]['capacity'] - Gf[edge[0]][edge[1]]['flow']
        Gf[edge[1]][edge[0]]['capacity'] = Gf[edge[0]][edge[1]]['flow']
        Gf[edge[0]][edge[1]]['flow'] = 0
        Gf[edge[1]][edge[0]]['flow'] = 0
    
    return Gf

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def fordFulkerson_(G, s, t):
    '''
    Inputs:
        G: a graph
        s: a source vertex
        t: a sink vertex
    Outputs:
        the graph G whose flow was modified by Ford-Fulkerson algorithm.
        In case there is no path from s to t, return None.
    '''
    # initialize flows
    for e in G.edges():
        G[e[0]][e[1]]['flow'] = 0
        
    # Forward edgesを記録
    forwardEdges = G.edges()
    
    # Residual Graphの作成
    Gf = makeResidualGraph(G)
    
    # そもそもGにおいてsからtへのパスがあるのか確認
    path = bfsFlowPath_(G, s, t)
    if path == None:
        print ("There is no path from " + str(s) + " to "+ str(t) )
        return None
    
    # Gにおいてsからtへのパスがある場合
    # ここもいじった
    while(1):
        path = bfsFlowPath_(Gf, s, t)
        if path == None:
            break
        else:
            # path上のedgeについて、capacity - flowの最小値を調べる
            min = float('inf')
            for edge in path:
                if ( min > Gf[edge[0]][edge[1]]['capacity']):
                    min = Gf[edge[0]][edge[1]]['capacity']
            
            # path上のedgeのflowを更新
            for edge in path:
                if edge in forwardEdges:
                    Gf[edge[0]][edge[1]]['flow'] += min
                    Gf[edge[0]][edge[1]]['capacity'] -= min
                    Gf[edge[1]][edge[0]]['capacity'] += min
                else:
                    Gf[edge[1]][edge[0]]['flow'] -= min
                    Gf[edge[0]][edge[1]]['capacity'] += min
    
    # もともと無かったedgeを消去
    for edge in Gf.edges():
        if not edge in forwardEdges:
            Gf.remove_edge(edge[0],edge[1])
    
    return Gf