import numpy as np


def simplex(c, A, b, basis, nonbasis, x=None):
    '''
    c: n x 1, A: m x n, b = m x 1
    x: n x 1, initial value
    basis: m x 1, nonbasis: (n-m) x 1

    c, A, b, x: numpy array
    basis, nonbasis: python list
    '''

    m = len(A)
    n = len(c)

    if x is None:
        x = np.array([0.0] * n)

    optVal = x.dot(c)

    # check feasibility
    for test in range(m):
        if (A.dot(x) > b)[test]:
            print('infeasible')
            return None

    # pivoting
    EPSILON = 10**(-5)
    TIME = 0
    while(np.max(c) > EPSILON):
        # choose j_pivot
        c_nonbasis = np.array([c[i] if i in nonbasis else -float('inf') for i in range(len(c))])
        j_pivot = np.argmax(c_nonbasis)

        # check boundedness
        a = np.max(A.T[j_pivot])
        if a <= 0:
            print('unbounded')
            return None

        # choose pivot
        pivot_column = [i / j if j != 0 else float('inf') for i, j in zip(b, A.T[j_pivot])]
        # pivot_column = b / A.T[j_pivot] としてもよいがdevided by zero errorがうるさい
        pivot_column = [pivot_column[i] if pivot_column[i] >= 0 else float('inf') for i in range(len(pivot_column))]
        i_pivot = np.argmin(pivot_column)
        stepsize = np.min(pivot_column)
        optVal += stepsize * c[j_pivot]

        # update basis and nonbasis
        nonbasis.append(basis[i_pivot])
        nonbasis.remove(j_pivot)
        basis[i_pivot] = j_pivot

        # update A, b, and c
        b[i_pivot], A[i_pivot] = b[i_pivot] / A[i_pivot][j_pivot], A[i_pivot] / A[i_pivot][j_pivot]
        A[i_pivot][j_pivot] = 0

        for i in range(m):
            if i != i_pivot:
                A[i] = A[i] - A[i_pivot] * A[i][j_pivot]
                b[i] = b[i] - b[i_pivot] * A[i][j_pivot]
                A[i][j_pivot] = 0

        c = c - A[i_pivot] * c[j_pivot]
        c[j_pivot] = 0

        # for debugging
        TIME += 1
        solution = [b[basis.index(i)] if i in basis else 0 for i in range(n)]
        print('loop no.{}: val = {}、sol = {}'.format(TIME, optVal, solution))
        if TIME > 100:
            break


    print('opt.val. = {}, opt.sol. = {}'.format(optVal, solution))
