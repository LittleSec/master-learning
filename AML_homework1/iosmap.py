import numpy as np
import scipy.sparse.csgraph as dij
import queue

global dataSet
dataSet = ['sonar', 'splice']


def loadData(fileName='sonar-train.txt'):
    return np.loadtxt(fileName, delimiter=',')  # m条n维数据


def euclideanDis(vec1, vec2):
    return np.sqrt(np.sum(np.power((vec1-vec2), 2)))  # 曼哈顿距离


def k1NN(vecPerdict, trainMatrix):
    '''
    m条n维
    vecPerdict: 1*n
    trainMatrix: n*m
    return index
    '''
    distances = []
    for i in range(trainMatrix.shape[1]):
        distances.append(euclideanDis(vecPerdict, trainMatrix[:, i]))
    return np.argmin(np.array(distances))  # return only a num


def culAccuracy(trainY, trainLabel, testY, testLabel):
    resBool = []
    for i in range(testY.shape[1]):
        vecPerdict = testY[:, i]
        resIndex = k1NN(vecPerdict, trainY)
        if testLabel[i] == trainLabel[resIndex]:
            resBool.append(True)
        else:
            resBool.append(False)
    acc = resBool.count(True) / len(resBool)
    return acc


def isConnect(G):
    '''
    G is numpy.ndarray
    '''
    cnt = 0
    numVertexes = G.shape[1]  # 图的顶点个数，即样本
    mark = [False] * numVertexes  # mark为标记数组，True为入队，False表示还未入队，初始化为False
    q = queue.Queue()
    q.put(0)
    mark[0] = True
    while not q.empty():
        v = q.get()
        mark[v] = True
        cnt += 1
        # print(cnt)
        for i in range(numVertexes):
            if (not np.isinf(G[v][i])) and (G[v][i] > 0) and (not mark[i]):
                q.put(i)
                mark[i] = True
    if cnt != numVertexes:
        return False
    else:
        return True

# 暂不使用，改用调库了scipy.sparse.csgraph.shortest_path()


def dijkstra(G, start):
    '''
    用Dijkstra算法求无向图G的v0顶点到其余顶点v的最短路径P[v]及其带权长度D[v]。
    若P[v][w]为TRUE，则w是从v0到v当前求得最短路径上的顶点。
    final[v]为TRUE当且仅当v∈S，即已经求得从v0到v的最短路径。
    根据本科C++代码改编
    '''
    numVertexes = G.shape[1]
    final = [False] * numVertexes
    D = []
    P = []
    for v in range(numVertexes):
        D.append(G[start][v])
        P.append([])
        for w in range(numVertexes):
            P[v].append(False)  # 设空路径
        if D[v] < np.inf:
            P[v][start] = True
            P[v][v] = True
    D[start] = 0
    final[start] = True  # 初始化，v0顶点属于S集
    # 开始主循环，每次求得v0到某个v顶点的最短路径，并加v到S集
    for i in range(1, numVertexes):  # 其余G.vexnum-1个顶点
        min_dis = np.inf  # 当前所知离v0顶点的最近距离
        for w in range(numVertexes):
            if not final[w]:  # w顶点在V-S中
                if D[w] < min_dis:  # w顶点离v0顶点更近
                    v = w
                    min_dis = D[w]
        final[v] = True  # 离v0顶点最近的v加入S集
        for w in range(numVertexes):  # 更新当前最短路径及距离
            if not final[w] and min_dis+G[v][w] < D[w]:  # 修改D[w]和P[w]，w∈V-S
                D[w] = min_dis + G[v][w]
                for j in range(numVertexes):
                    P[w][j] = P[v][j]
                P[w][w] = True  # P[w]=P[v]+[w]
    return D


def MDS(D, k):
    '''
    '''
    DSquare = D ** 2
    totalMean = np.mean(DSquare)
    columnMean = np.mean(DSquare, axis=0)
    rowMean = np.mean(DSquare, axis=1)
    B = np.zeros(DSquare.shape)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            B[i][j] = -0.5 * (DSquare[i][j] - rowMean[i] -
                              columnMean[j] + totalMean)
    eigVal, eigVec = np.linalg.eig(B)  # 求特征值及特征向量
    # 对特征值进行排序，得到排序索引
    eigValSorted_indices = np.argsort(eigVal)
    # 提取d个最大特征向量
    topd_eigVec = eigVec[:, eigValSorted_indices[:-k-1:-1]]  # -d-1前加:才能向左切
    X = np.dot(topd_eigVec, np.sqrt(np.diag(eigVal[:-k-1:-1])))
    return X


if __name__ == "__main__":
    '''
    data set: sonar
        k=10, accuracy=0.5631067961165048
        k=20, accuracy=0.6019417475728155
        k=30, accuracy=0.46601941747572817
    data set: splice
        k=10, accuracy=0.76
        k=20, accuracy=0.7425287356321839
        k=30, accuracy=0.7282758620689656
    '''
    for ds in dataSet:
        print("=============== "+ds+" ===============")

        trainData = loadData(ds+'-train.txt')  # m条n维
        trainLabel = trainData[:, -1]
        trainData = trainData[:, :-1]

        testData = loadData(ds+'-test.txt')
        testLabel = testData[:, -1]
        testData = testData[:, :-1]

        for kk in [10, 20, 30]:
            k1 = 4  # 连通k
            k2 = 4

            # 创建图，节点数是是样本个数
            numVertexes = trainData.shape[0]
            G = np.zeros((numVertexes, numVertexes))
            for i in range(numVertexes):
                for j in range(i+1, numVertexes):
                    G[i][j] = G[j][i] = euclideanDis(
                        trainData[i], trainData[j])

            for k1 in range(k1, numVertexes):
                # 保留k邻近点
                G_knn = np.copy(G)
                for i in range(numVertexes):
                    index = np.argsort(G[i])  # 小-->大
                    for j in index[:-k1]:
                        if i != j:
                            G_knn[i][j] = np.inf
                            # if index = np.argsort(G_knn[i]) then
                            # can't not G_knn[i][j]= G_knn[j][i] = np.inf, because later value will use to sort
                # print(k)
                if isConnect(G_knn):
                    print("train_k =", k1)
                    G_dist = dij.shortest_path(G_knn, directed=False)
                    # G_dist = np.full(G_knn.shape, np.inf)
                    # for i in range(G.shape[0]):
                    #     G_dist[i] = dijkstra(G_knn, i)
                    break

            train_Y = MDS(G_dist, kk)

            # 创建图，节点数是是样本个数
            numVertexes = testData.shape[0]
            G = np.zeros((numVertexes, numVertexes))
            for i in range(numVertexes):
                for j in range(i+1, numVertexes):
                    G[i][j] = G[j][i] = euclideanDis(testData[i], testData[j])

            for k2 in range(k2, numVertexes):
                # 保留k邻近点
                G_knn = np.copy(G)
                for i in range(numVertexes):
                    index = np.argsort(G[i])
                    for j in index[:-k2]:
                        if i != j:
                            G_knn[i][j] = np.inf
                            # if index = np.argsort(G_knn[i]) then
                            # can't not G_knn[i][j]= G_knn[j][i] = np.inf, because later value will use to sort
                # print(k)
                if isConnect(G_knn):
                    print("test_k =", k2)
                    G_dist = dij.shortest_path(G_knn, directed=False)
                    # G_dist = np.full(G_knn.shape, np.inf)
                    # for i in range(G.shape[0]):
                    #     G_dist[i] = dijkstra(G_knn, i)
                    break

            test_Y = MDS(G_dist, kk)

            accuracy = culAccuracy(train_Y.T, trainLabel, test_Y.T, testLabel)
            print("   k={0}, accuracy={1}".format(kk, accuracy))
