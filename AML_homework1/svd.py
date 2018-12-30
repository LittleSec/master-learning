import numpy as np

global dataSet
dataSet = ['sonar', 'splice']

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


def SVDdimReduct():
    '''
    data set: sonar
        k=10, accuracy=0.6019417475728155
        k=20, accuracy=0.5728155339805825
        k=30, accuracy=0.5631067961165048
    data set: splice
        k=10, accuracy=0.76
        k=20, accuracy=0.7425287356321839
        k=30, accuracy=0.7282758620689656
    '''
    for ds in dataSet:
        print("data set: " + ds)
        trainData = loadData(ds+'-train.txt') # m条n维
        trainLabel = trainData[:,-1]
        trainData = trainData[:, :-1] # m*n

        testData = loadData(ds+'-test.txt')
        testLabel = testData[:,-1]
        testData = testData[:, :-1]
        
        train_U, train_S, train_V = np.linalg.svd(trainData)
        for k in [10, 20, 30]:
            P = train_V[:k,:].T
            train_Y = np.dot(trainData, P)
            test_Y = np.dot(testData, P)
            accuracy = culAccuracy(train_Y.T, trainLabel, test_Y.T, testLabel)
            print("   k={0}, accuracy={1}".format(k, accuracy))

if __name__ == "__main__":
    SVDdimReduct()