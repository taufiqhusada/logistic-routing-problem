import heapq 
from math import inf, isfinite
import datetime

mapNode = {}

def findShortestPath(a, b, adjMatrixAll):
    begin_time = datetime.datetime.now()
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
            for v in range(6105):
                if (isfinite(adjMatrixAll[u][v])):
                    if (dist[v] > dist[u] + adjMatrixAll[u][v]):
                        dist[v] = dist[u] + adjMatrixAll[u][v]
                        pred[v] = u
                        heapq.heappush(pq, (dist[v],v))
    
    print(datetime.datetime.now() - begin_time)

    # find path dari a -> b
    nodeNow = b
    while(nodeNow!=-1):
        path.append(nodeNow)
        nodeNow = pred[nodeNow]
    path = path[::-1]
    
    return dist[b], path

def getEdgeDataFromFile():
    adjMatrixAll = [[inf for i in range(6105)] for i in range(6105)]
    fEdge = open('../data/EdgeData.txt', 'r').readlines()
    for i in range(6105):
        for j in range(6105):
            if(i==j):
                adjMatrixAll[i][j] = 0

    for line in fEdge:
        parseLine = [x for x in line.split()]
        u = int(parseLine[1])
        v = int(parseLine[2])
        weight = float(parseLine[3])
        adjMatrixAll[u][v] = weight
        adjMatrixAll[v][u] = weight
    
    return adjMatrixAll

def initSubGraph(nodeKantor, listNodeTujuan, adjMatrixAll):
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
                    dist, path = findShortestPath(u,v,adjMatrixAll)
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
    for i in range(nTujuan):
        mapNode[listNodeTujuan[i]] = i+1

    adjMatrixAll = getEdgeDataFromFile()
    
    adjMatrixSubGraph, listPath = initSubGraph(nodeKantor, listNodeTujuan, adjMatrixAll)
    
    # print
    print("done")
    listNodeTujuan.append(nodeKantor)
    for u in listNodeTujuan:
        print(u, " ", adjMatrixSubGraph[mapNode[u]])
        print(listPath[mapNode[u]])

if __name__ == "__main__":
    init()