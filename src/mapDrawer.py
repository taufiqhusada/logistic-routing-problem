import matplotlib.pyplot as plt
from tqdm import tqdm

# fungsi untuk mendapatkan data node dari file
def getCoorNodesFromFile(cityOption):
    coorNodes = []
    fNodes = open(f'../data/{cityOption}/NodeData.txt', 'r').readlines()
    for line in fNodes:
        parseLine = [x for x in line.split()]
        x = float(parseLine[1])
        y = float(parseLine[2])
        coorNodes.append((x,y))        
    return coorNodes

# fungsi untuk draw map nya
def drawMap(adjListAll, mapNodeToIdx, listPath, jumlahKurir, resTSPkurir, cntAllNode, cityOption):
    coorNodes = getCoorNodesFromFile(cityOption)

    if (cityOption=="Oldenburg"):
        #print all map
        for i in tqdm(range(cntAllNode)):
            if (len(adjListAll[i])!=0):
                for v in adjListAll[i]:
                    x1 = coorNodes[i][0]
                    y1 = coorNodes[i][1]
                    x2 = coorNodes[v][0]
                    y2 = coorNodes[v][1]
                    plt.plot([x1,x2],[y1,y2],color="k")

    listColor=['c','r','y','m','g','b']

    for i in tqdm(range(jumlahKurir)):
        for pairNode in resTSPkurir[i]:
            path = listPath[mapNodeToIdx[pairNode[0]]][mapNodeToIdx[pairNode[1]]]
            predNode = path[0]
            for nodes in path:
                x1 = coorNodes[predNode][0]
                y1 = coorNodes[predNode][1]
                x2 = coorNodes[nodes][0]
                y2 = coorNodes[nodes][1]
                plt.plot([x1,x2],[y1,y2],color=listColor[i%6])

                predNode = nodes
           
    
    plt.show()