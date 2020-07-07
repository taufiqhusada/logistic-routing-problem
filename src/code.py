import heapq 
from math import inf, isfinite
import datetime
from solver import solveTSP
from mapDrawer import drawMap
from tqdm import tqdm

mapNodeToIdx = {} # map node ke index
mapIdxToNode = {} # map idx ke node

# fungsi untuk find shortest path antar node a dan b
# metode djikstra berdasarkan referensi psudocode dari buku "Pemrograman Kompetitif Dasar"
def findShortestPath(a, b, adjListAll, cntAllNode):
    path = []
    
    dist = [inf for i in range(cntAllNode)]
    pred = [-1 for i in range(cntAllNode)]
    isVisited = [False for i in range(cntAllNode)]

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

    # find path dari a -> b
    nodeNow = b
    while(nodeNow!=-1):
        path.append(nodeNow)
        nodeNow = pred[nodeNow]
    path = path[::-1]
    
    return dist[b], path

# fungsi untuk mengambil edge data dari file txt
def getEdgeDataFromFile(cityOption, cntAllNode):
    adjListAll = [{} for i in range(cntAllNode)]
    fEdge = open(f'../data/{cityOption}/EdgeData.txt', 'r').readlines()
    for i in range(cntAllNode):
        adjListAll[i][i] = 0

    for line in tqdm(fEdge):
        parseLine = [x for x in line.split()]
        u = int(parseLine[1])
        v = int(parseLine[2])
        weight = float(parseLine[3])
        adjListAll[u][v] = weight
        adjListAll[v][u] = weight
    
    return adjListAll

# fungsi untuk inisialisasi sub graph
def initSubGraph(nodeKantor, listNodeTujuan, adjListAll, cntAllNode):
    listPath = [[[] for i in range(len(listNodeTujuan)+1)] for e in range(len(listNodeTujuan)+1)]
    adjMatrixSubGraph = [[inf for i in range(len(listNodeTujuan)+1)] for e in range(len(listNodeTujuan)+1)]

    listNodeTujuan.append(nodeKantor)   #sementara aja

    for u in tqdm(listNodeTujuan):
        for v in listNodeTujuan:
            uMapped = mapNodeToIdx[u]
            vMapped = mapNodeToIdx[v]
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
                    dist, path = findShortestPath(u,v,adjListAll,cntAllNode)
                    # print(dist)
                    adjMatrixSubGraph[uMapped][vMapped] = dist
                    listPath[uMapped][vMapped] = path    

                

    listNodeTujuan.pop()

    return adjMatrixSubGraph, listPath

# binary search, credit to geeksForGeeks
def binarySearch(arr, x, n):
    low = 0
    high = n-1
    while(low<=high):
        mid = (high+low)//2
        if arr[mid][0] < x: 
            low = mid + 1
        elif arr[mid][0] > x: 
            high = mid - 1
        else: 
            return mid 
    return -1

# fungsi utama
def exec():
    # proses input
    print('masukkan pilihan kota (1. Oldenburg, 2. SanFrancisco): ', end='')
    optNumber = int(input())
    cityOption = ""
    cntAllNode = 0
    if (optNumber==2):
        cityOption = "SanFrancisco"
        cntAllNode = 174956
    else:
        cityOption = "Oldenburg"
        cntAllNode = 6105

    print('masukkan simpul kantor pusat:', end=' ')
    nodeKantor = int(input())
    print('masukkan jumlah titik tujuan:', end=' ')
    nTujuan = int(input())
    print('masukkan titik-titik tujuan (pisahkan dengan spasi)')
    listNodeTujuan = [int(x) for x in input().split()]
    print('masukkan jumlah kurir:', end=' ')
    jumlahKurir = int(input())
    
    #node mapping
    mapNodeToIdx[nodeKantor] = 0
    mapIdxToNode[0] = nodeKantor
    for i in range(nTujuan):
        mapNodeToIdx[listNodeTujuan[i]] = i+1
        mapIdxToNode[i+1] = listNodeTujuan[i]

    adjListAll = getEdgeDataFromFile(cityOption, cntAllNode)
    
    adjMatrixSubGraph, listPath = initSubGraph(nodeKantor, listNodeTujuan, adjListAll, cntAllNode)
    
    # print
    print("done")

    # single TSP
    resSingleTSP = solveTSP(adjMatrixSubGraph, listPath, nodeKantor, listNodeTujuan, mapIdxToNode,mapNodeToIdx)    
    print(resSingleTSP)

    # clustering

    # sort list node
    resSingleTSP.sort() # disort dulu supaya bisa di binary search nantinya
    print(resSingleTSP)
    idx = binarySearch(resSingleTSP,nodeKantor,len(resSingleTSP))   # cari idx node kantor
    orderedListNodeTujuan = []
    nextNode = resSingleTSP[idx][1]     # simpen node setelah node kantor
    for i in range(1,len(resSingleTSP)):
        idx = binarySearch(resSingleTSP,nextNode,len(resSingleTSP))
        orderedListNodeTujuan.append(resSingleTSP[idx][0])
        nextNode = resSingleTSP[idx][1]
    print(orderedListNodeTujuan)

    # bagi node nya sama rata
    idxNow = 0
    listNodeEveryKurir = []
    for i in range(jumlahKurir):
        jumlahNode = nTujuan//jumlahKurir + (1 if i < nTujuan % jumlahKurir else 0) 
        temp = []
        maxIdx = jumlahNode+idxNow
        while(idxNow<maxIdx):
            temp.append(orderedListNodeTujuan[idxNow])
            idxNow+=1
        listNodeEveryKurir.append(temp)
    
    print(listNodeEveryKurir)

    resTSPkurir = []
    for i in range(jumlahKurir):
        resTSPkurir.append(solveTSP(adjMatrixSubGraph, listPath, nodeKantor, listNodeEveryKurir[i], mapIdxToNode, mapNodeToIdx))
    
    # ouput 
    print("--------------------------------------------")
    print(listNodeEveryKurir)
    print(resTSPkurir)   
    print("--------------------------------------------")
    print("RESULT")
    print("--------------------------------------------")
    for i in range(jumlahKurir):
        print(f"kurir-{i+1}")
        totalCost = 0
        for pairNode in resTSPkurir[i]:
            print(pairNode[0]," -> ",pairNode[1]," : ", listPath[mapNodeToIdx[pairNode[0]]][mapNodeToIdx[pairNode[1]]] )
            totalCost += adjMatrixSubGraph[mapNodeToIdx[pairNode[0]]][mapNodeToIdx[pairNode[1]]]
        print(f"\nTotal Cost : {totalCost}")
        print("--------------------------------------------")
         
    # draw map
    drawMap(adjListAll, mapNodeToIdx, listPath, jumlahKurir, resTSPkurir, cntAllNode, cityOption)


if __name__ == "__main__":
    exec()