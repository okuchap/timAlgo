def Initialize(G, s, t):
    '''
    Inputs:
        G: a graph
            V: verteces
                height
                excess
            E: edges
                flow(preflow)
                capacity
                    NB: flow <= capacity
        s: a start point
        t: an end point
    Output:
        H: modified graph
    
    Initialize the height and excess of each vertex.
    '''
    H = G.copy()
    for v in H.nodes():
        H.node[v]['excess'] = 0

    for v in H.nodes():
        # 始点以外の点について
        if v != s:
            H.node[v]['height'] = 0
            # H.node[v]['excess'] = 0
            for p in H.neighbors(v):
                H[v][p]['flow'] = 0
        # 始点について
        else:
            # 始点の高さをnに
            H.node[v]['height'] = H.number_of_nodes() # n
            # 始点から出る枝のpreflowをcapacityギリギリに
            # このとき、始点に隣接する点のexcessを更新
            for p in H.neighbors(v):
                H[v][p]['flow'] = H[v][p]['capacity']
                H.node[p]['excess'] = H[v][p]['flow']
                
    return H

def Push(G, v, w, forwardEdges):
    '''
    G: a graph(a residual graph)
    v, w: vertices of G such that h(v) = h(w) + 1
    forwardEdges: a list of the edges of the original graph
    '''

    # 更新量diffを計算
    residualCapacity = G[v][w]['capacity'] - G[v][w]['flow']
    diff = np.min([G.node[v]['excess'], residualCapacity])

    # (v,w), (w,v)を更新, p.3を参考に
    if (v,w) in forwardEdges:
        G[v][w]['flow'] += diff
        G[w][v]['capacity'] += diff
        G.node[v]['excess'] -= diff
        G.node[w]['excess'] += diff
    else:
        G[v][w]['flow'] -= diff
        G[w][v]['capacity'] -= diff
        G.node[v]['excess'] += diff
        G.node[w]['excess'] -= diff

def loopCondition(G, s, t):
    nodelist = G.nodes()
    nodelist.remove(s)
    nodelist.remove(t)

    for v in nodelist:
        if(G.node[v]['excess'] > 0):
            return True
    return False

def PushRelabel(G, s, t):
    '''
    Inputs:
        G: a graph
        s: a starting point
        t: an end point
    Output:
        the graph G with its maximum flow
    '''

    # Forward Edges を記録
    forwardEdges = G.edges()

    # s,tを除いたnodeのlistを作る
    nodeList = G.nodes()
    nodeList.remove(s)
    nodeList.remove(t)

    # residual graph の作成
    Gf = makeResidualGraph(G)

    # Initialization
    Initialize(Gf, s, t)

    # Main Loop
    while(loopCondition(Gf, s, t)):
        # 高さが最も高く、かつexcess > 0の点を探す
        height = -100 # 適当に負の値を設定
        for p in nodeList:
            if(Gf.node[p]['excess'] > 0 and Gf.node[p]['height'] > height):
                v = p
                height = Gf.node[p]['height']

        # h(v) = h(w) + 1 を満たす点wを探す
        w = None
        for p in Gf.nodes():
            if(Gf.node[v]['height'] == Gf.node[p]['height'] + 1 and (Gf[v][p]['capacity'] - Gf[v][p]['flow']) > 0):
                w = p
                break

        # そのような点wがない場合、increment h(v)
        if w == None:
            Gf.node[v]['height'] += 1

        # ある場合
        else:
            Push(Gf, v, w, forwardEdges)

    # もともと無かったedgeを消去
    for edge in Gf.edges():
        if not edge in forwardEdges:
            Gf.remove_edge(edge[0],edge[1])
    
    return Gf