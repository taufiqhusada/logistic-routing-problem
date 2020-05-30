from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY


def solve(adjMatrixSubGraph, listPath, nodeKantor, listNodeTujuan, mapIdx, m, p):
    model = Model()
    n = len(listNodeTujuan)
    
    # add variable
    x = [[model.add_var(var_type=BINARY) for j in range(n+1)] for i in range(n+1)]
    y = [model.add_var() for i in range(n+1)]

    # add objective function
    model.objective = minimize(xsum(adjMatrixSubGraph[i][j]*x[i][j] for i in range(n+1) for j in range(n+1)))

    # constraint: Ensure that exactly m salesmen depart from node kantor
    model += xsum(x[0][j] for j in range(1,n+1)) == m

    # constraint: Ensure that exactly m salesmen return to node kantor
    model += xsum(x[j][0] for j in range(1,n+1)) == m

    V = set(range(n+1))
    # constraint : leave each city only once
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1

    # constraint : enter each city only once
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1

    # subtour elimination
    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - y[j] + p*x[i][j] <= p-1

    # optimizing
    model.optimize(max_seconds=10000)

    # checking if a solution was found
    if model.num_solutions:
        print("SOLUTION FOUND")
        for i in range(n+1):
            for j in range(n+1):
                if (x[i][j].x==1):
                    print(mapIdx[i]," ",mapIdx[j]," : ", listPath[i][j])

    else:
        print("gak ketemu")