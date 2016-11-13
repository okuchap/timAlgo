def bfsFlowPath(G, s, e):
    '''
    Search a path from s to t all of whose points have strictly positive capacity.
    
    Inputs:
        G: a graph
        s: a start point
        e: an end point
        each edge has two attributes:
            capacity: capacity
            flow: its current flow which should be no more than its capacity
    Output:
        path: a list of edges which represents a path from s to e.
        At each edge of the path, its current flow is strictly less than its capacity.
        In case there is no path from s to t, return None.
    '''

    # 過去に訪れた点を記録
    # sは最初から入れておく
    past = [s]
    # pathを記録するためのリスト
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
        # current flow < capacity となるedgeだけをpathの候補に
        # flow < capacity となるedge以外は存在しないものとして扱うのと同じ
        if G[s][p]['flow'] < G[s][p]['capacity']:
            queue.append(p)
            
    # あとで条件分岐に用いる
    numberOfSuccessorsOfSource = len(queue)
    
    # sに隣接する点の距離を1に
    for p in queue:
        G.node[p]['dist'] = 1

    # BFSを用いてflow < capacityを満たすsからeへのpathがあるのか調べる
    # pastに過去に訪れた点を格納
    while len(queue)>0:
        v = queue.popleft()
        if v == e: break
        else:
            past.append(v)
            for p in G.successors(v):
                # (過去に訪れていない and flow < capacity)を満たすedge
                if ( (not p in past) and ( G[v][p]['flow'] < G[v][p]['capacity']) ):
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
            # distの作り方から、flow < capは自然に満たされる???
            if ( G.node[p]['dist'] == G.node[pp]['dist']-1 and G[p][pp]['flow'] < G[p][pp]['capacity']):
                path.insert(0, (p,pp))
                pp = p
                break
            else:
                count += 1
        
        # 条件を満たすedgeがない
        if count == len(pred):
            break

    return path