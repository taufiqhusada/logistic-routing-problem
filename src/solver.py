from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY

# solve single TSP dengan MIP
# credit to https://python-mip.readthedocs.io/en/latest/intro.html
def solveTSP(adjMatrixSubGraph, listPath, nodeKantor, listNode, mapIdxToNode, mapNodeToIdx):
    model = Model()
    listNode.insert(0,nodeKantor)
    n = len(listNode)

    # add variable
    x = [[model.add_var(var_type=BINARY) for j in range(n)] for i in range(n)]
    y = [model.add_var() for i in range(n)]

    # add objective function
    model.objective = minimize(xsum(adjMatrixSubGraph[mapNodeToIdx[listNode[i]]][mapNodeToIdx[listNode[j]]]*x[i][j] for i in range(n) for j in range(n)))

    V = set(range(n))
    # constraint : leave each city only once
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1

    # constraint : enter each city only once
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1


    # subtour elimination
    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n

    # optimizing
    model.optimize(max_seconds=30)


    res = []
    # checking if a solution was found
    if model.num_solutions:
        print("SOLUTION FOUND")
        for i in range(n):
            for j in range(n):
                if (x[i][j].x==1):
                    print(listNode[i]," ",listNode[j]," : ", listPath[mapNodeToIdx[listNode[i]]][mapNodeToIdx[listNode[j]]])
                    res.append((listNode[i],listNode[j]))

        

    else:
        print("gak ketemu")
    return res