import numpy
class B:
    def __init__(self):
        pass

    def manhattanDis(self, v1, v2):
        return numpy.sqrt(numpy.sum(numpy.fabs(v1-v2))) # 曼哈顿距离
    
    def euclideanDis(self, v1, v2):
        return numpy.sqrt(numpy.sum(numpy.power((v1-v2), 2)))  # 欧氏距离
