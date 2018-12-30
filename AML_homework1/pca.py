import numpy as np

global dataSet
dataSet = ['sonar', 'splice']

def pac(data):
    '''
    data: n行m列矩阵，m条n维数据
    '''
    data_m = np.mean(data, axis=1) # 每一行均值
    data_X = data - data_m.reshape((data_m.shape[0], 1)) # 零均值化
    # covC = np.cov(data_m) # 协方差矩阵，理论上=1/m * XXT
    covC = np.dot(data_X, data_X.T) / data_X.shape[1]
    featValue, featVec = np.linalg.eig(covC) # 协方差矩阵的特征值及对应的特征向量
    # 将特征向量按对应特征值大小从上到下按行排列成投影矩阵
    index = np.argsort(featValue) # 对特征值小-->大，返回下标
    eigValsIndex = index[::-1] # big-->small
    P = featVec[eigValsIndex, :]
    return P

def loadData(fileName='sonar-train.txt'):
    return np.loadtxt(fileName, delimiter=',') # m条n维数据

def manhattanDis(vec1, vec2):
    return np.sqrt(np.sum(np.fabs(vec1-vec2))) # 曼哈顿距离

def k1NN(vecPerdict, trainMatrix):
    '''
    m条n维
    vecPerdict: 1*n
    trainMatrix: n*m
    return index
    '''
    distances = []
    for i in range(trainMatrix.shape[1]):
        distances.append(manhattanDis(vecPerdict, trainMatrix[:,i]))
    return np.argmin(np.array(distances)) # return only a num(index)
    
def dimReduce(trainData, testData, k=10):
    '''
    m条n维
    trainData: n*m, no labels
    testData: n*m, no labels
    '''
    P = pac(trainData)
    trainY = np.dot(P[:k], trainData)
    testY = np.dot(P[:k], testData)
    return trainY, testY

def culAccuracy(trainY, trainLabel, testY, testLabel):
    resBool = []
    for i in range(testY.shape[1]):
        vecPerdict = testY[:,i]
        resIndex = k1NN(vecPerdict, trainY)
        if testLabel[i] == trainLabel[resIndex]:
            resBool.append(True)
        else:
            resBool.append(False)
    acc = resBool.count(True) / len(resBool)
    return acc

def PCAdimReduct():
    '''
    data set: sonar
        k=10, accuracy=0.5048543689320388
        k=20, accuracy=0.4854368932038835
        k=30, accuracy=0.5339805825242718
    data set: splice
        k=10, accuracy=0.5995402298850575
        k=20, accuracy=0.6308045977011494
        k=30, accuracy=0.6574712643678161
    '''
    for ds in dataSet:
        print("data set: " + ds)
        trainData = loadData(ds+'-train.txt') # m条n维
        trainLabel = trainData[:,-1]
        trainData = trainData[:, :-1].T # 按列组成n行m列矩阵

        testData = loadData(ds+'-test.txt')
        testLabel = testData[:,-1]
        testData = testData[:, :-1].T # n*m

        for k in [10, 20, 30]:
            trainY, testY = dimReduce(trainData, testData, k)
            accuracy = culAccuracy(trainY, trainLabel, testY, testLabel)
            print("   k={0}, accuracy={1}".format(k, accuracy))



if __name__ == "__main__":
    PCAdimReduct()