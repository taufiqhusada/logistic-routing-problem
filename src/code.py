import heapq 
from math import inf, isfinite
import datetime
from solver import solve

mapNode = {} #node ke index
mapIdx = {} # idx ke node

def findShortestPath(a, b, adjListAll):
    # begin_time = datetime.datetime.now()
    path = []
    # djikstra from a 
    # (berdasarkan referensi psudocode dari buku "Pemrograman Kompetitif Dasar")
    dist = [inf for i in range(6105)]
    pred = [-1 for i in range(6105)]
    isVisited = [False for i in range(6105)]

    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq,(0,a))
    dist[a] = 0
    while(len(pq)!=0):
        (curDist, u) = heapq.heappop(pq)
        if (not isVisited[u]):
            isVisited[u] = True
            for v in adjListAll[u]:
                if (dist[v] > dist[u] + adjListAll[u][v]):
                    dist[v] = dist[u] + adjListAll[u][v]
                    pred[v] = u
                    heapq.heappush(pq, (dist[v],v))
    
    # print(datetime.datetime.now() - begin_time)

    # find path dari a -> b
    nodeNow = b
    while(nodeNow!=-1):
        path.append(nodeNow)
        nodeNow = pred[nodeNow]
    path = path[::-1]
    
    return dist[b], path

def getEdgeDataFromFile():
    adjListAll = [{} for i in range(6105)]
    fEdge = open('../data/EdgeData.txt', 'r').readlines()
    for i in range(6105):
        for j in range(6105):
            if(i==j):
                adjListAll[i][j] = 0

    for line in fEdge:
        parseLine = [x for x in line.split()]
        u = int(parseLine[1])
        v = int(parseLine[2])
        weight = float(parseLine[3])
        adjListAll[u][v] = weight
        adjListAll[v][u] = weight
    
    return adjListAll

def initSubGraph(nodeKantor, listNodeTujuan, adjListAll):
    listPath = [[[] for i in range(len(listNodeTujuan)+1)] for e in range(len(listNodeTujuan)+1)]
    adjMatrixSubGraph = [[inf for i in range(len(listNodeTujuan)+1)] for e in range(len(listNodeTujuan)+1)]

    listNodeTujuan.append(nodeKantor)   #sementara aja

    for u in listNodeTujuan:
        print("process: find all distance from ", u)
        for v in listNodeTujuan:
            uMapped = mapNode[u]
            vMapped = mapNode[v]
            if (u==v):
                adjMatrixSubGraph[uMapped][vMapped] = 0
                listPath[uMapped][vMapped] = [u]
            else:
                if (isfinite(adjMatrixSubGraph[vMapped][uMapped])):
                    adjMatrixSubGraph[uMapped][vMapped] = adjMatrixSubGraph[vMapped][uMapped]
                    path = []
                    for e in reversed(listPath[vMapped][uMapped]):
                        listPath[uMapped][vMapped].append(e)
                else:
                    dist, path = findShortestPath(u,v,adjListAll)
                    # print(dist)
                    adjMatrixSubGraph[uMapped][vMapped] = dist
                    listPath[uMapped][vMapped] = path    

                

    listNodeTujuan.pop()

    return adjMatrixSubGraph, listPath

def init():
    print('masukkan simpul kantor pusat:', end=' ')
    nodeKantor = int(input())
    print('masukkan jumlah titik tujuan:', end='')
    nTujuan = int(input())
    print('masukkan titik-titik tujuan (pisahkan dengan spasi)')
    listNodeTujuan = [int(x) for x in input().split()]
    
    #node mapping
    mapNode[nodeKantor] = 0
    mapIdx[0] = nodeKantor
    for i in range(nTujuan):
        mapNode[listNodeTujuan[i]] = i+1
        mapIdx[i+1] = listNodeTujuan[i]

    adjListAll = getEdgeDataFromFile()
    
    adjMatrixSubGraph, listPath = initSubGraph(nodeKantor, listNodeTujuan, adjListAll)
    
    # print
    print("done")
    # listNodeTujuan.append(nodeKantor)
    # for u in listNodeTujuan:
    #     print(u, " ", adjMatrixSubGraph[mapNode[u]])
    #     print(listPath[mapNode[u]])

    solve(adjMatrixSubGraph, listPath, nodeKantor, listNodeTujuan, mapIdx, 2, len(listNodeTujuan)+1)    

if __name__ == "__main__":
    init()