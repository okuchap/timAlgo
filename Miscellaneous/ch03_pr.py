def PushRelabel_new(G, s, t):
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
        # 高さが最も高く、かつexcess > 0の点vを探す
        height = -100 # 適当に負の値を設定
        for p in nodeList:
            if(Gf.node[p]['excess'] > 0 and Gf.node[p]['height'] > height):
                v = p
                height = Gf.node[p]['height']

        # h(v) = h(w) + 1 を満たす点wを探す
        # vのneighborsの中から探す(そうじゃないとkey eroorに)
        w = None
        for p in Gf.neighbors(v):
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


def Push(G, v, w, forwardEdges):
    '''
    G: a graph(a residual graph)
    v, w: vertices of G such that h(v) = h(w) + 1
    forwardEdges: a list of the edges of the original graph
    
    augment the flow of (v,w)
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