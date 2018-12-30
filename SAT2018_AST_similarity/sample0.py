import numpy as np
class A:
    def __init__(self):
        pass

    def manhattanDis(self, vec1, vec2):
        return np.sqrt(np.sum(np.fabs(vec1-vec2))) # 曼哈顿距离
    
    def euclideanDis(self, vec1, vec2):
        return np.sqrt(np.sum(np.power((vec1-vec2), 2))) # 欧氏距离
