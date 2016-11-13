import numpy as np

def fordFulkerson_(G, s, t):
    '''
    Inputs:
        G: a graph
        s: a source vertex
        t: a sink vertex
    Outputs:
        the graph G whose flow was modified by Ford-Fulkerson algorithm
        In case there is no path from s to t, return None.
    '''

    '''
    # initialize flows
    for e in G.edges():
        G[e[0]][e[1]]['flow'] = 0
    '''

    # Forward edgesを記録
    forwardEdges = G.edges()
    
    # Residual Graphの作成
    Gf = makeResidualGraph(G)
    
    # そもそもGにおいてsからtへのパスがあるのか確認
    path = bfsFlowPath(G, s, t)
    if path == None:
        print ("There is no path from " + str(s) + " to "+ str(t) )
        return None
    
    # Gにおいてsからtへのパスがある場合
    while(1):
        # これ以上パスがみつからない場合は最適なのでそこでループを打ち切る
        path = bfsFlowPath(Gf, s, t)
        if path == None:
            break

        # まだパスがある（最適でない）場合
        else:
            # path上のedgeについて、capacity - flowの最小値を調べる
            diff = float('inf')
            for edge in path:
                diff = np.min([diff, Gf[edge[0]][edge[1]]['capacity'] - Gf[edge[0]][edge[1]]['flow'] ])
            
            # path上のedgeのflowを更新
            for edge in path:
                if edge in forwardEdges:
                    Gf[edge[0]][edge[1]]['flow'] += diff
                    # このとき、backward edgeのcapacityを更新する必要あり？
                    Gf[edge[1]][edge[0]]['capacity'] += diff
                else:
                    Gf[edge[0]][edge[1]]['flow'] -= diff
                    Gf[edge[1]][edge[0]]['capacity'] -= diff
    
    # もともと無かったedgeを消去
    for edge in Gf.edges():
        if not edge in forwardEdges:
            Gf.remove_edge(edge[0],edge[1])
    
    return Gf