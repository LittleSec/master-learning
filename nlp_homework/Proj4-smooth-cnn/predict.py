from keras.layers.core import Dense, Flatten, Dropout, SpatialDropout1D
from keras.layers.convolutional import Conv1D
from keras.layers.embeddings import Embedding
from keras.layers.pooling import GlobalAveragePooling1D
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import collections
import numpy as np
import pickle
import os
import time

PKL_FILE = r"idmapword.pkl"
TXT_INPUT = r"pre_test_v3.txt"
TXT_OUTPUT = r'MF1833026.txt'
MODEL_FILE = r"model1.h5"
EMBED_SIZE = 100 # 网络中嵌入层生成的向量的大小
NUM_FILTERS = 128 # 卷积层训练的卷积滤波器的数目
NUM_WORDS = 6 # 每个滤波器的大小，即每次我们将卷积多少个词
BATCH_SIZE = 64 # 每次送入网络的记录的数量
NUM_EPOCHS = 10 # 训练中对整个数据集的所有样例重复运行的次数
MAX_LEN = 0 # 最大的句子长度
VOCAB_SIZE = 0 # 字典的大小，即词个数

def getIdMapWord():
    with open(PKL_FILE, mode="rb") as fr:
        word2index = pickle.load(fr)
    # 设置全局参数并删除字段
    global MAX_LEN
    MAX_LEN = word2index["<global_parameter>"]["MAX_LEN"]
    global VOCAB_SIZE
    VOCAB_SIZE = word2index["<global_parameter>"]["VOCAB_SIZE"]
    del word2index["<global_parameter>"]
    
    return word2index

def getTestX(word2index):
    xs = []
    with open(TXT_INPUT, mode='r', encoding="utf-8") as fr:
        for line in fr.readlines():
            splitline = str(line).strip().split('\t')
            words = splitline[1].split(' ')
            for word in words:
                wid = []
                if word in word2index:
                    wid.append(word2index[word])
                else:
                    wid.append(word2index["<OOV>"]) # 在训练集中没有的词
                xs.append(wid)
    X = pad_sequences(xs, maxlen=MAX_LEN)
    return X

def loadModel():
    print(MAX_LEN)
    print(VOCAB_SIZE)
    model = Sequential()
    model.add(Embedding(VOCAB_SIZE, EMBED_SIZE, input_length=MAX_LEN))
    model.add(SpatialDropout1D(0.2))
    model.add(Conv1D(filters=NUM_FILTERS, kernel_size=NUM_WORDS, padding="valid", activation="relu"))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(1, activation="sigmoid"))
    # model.add(Dense(2, activation="softmax"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])    
    # model.summary()
    model.load_weights(MODEL_FILE)
    return model

def predictTestY(model, testX):
    # raw = model.predict_classes(testX)
    raw = model.predict(testX)
    # print(raw)
    # raw = raw.astype("int") # 要注意了，0.1就会成为0
    res = []
    for r in [r[0] for r in raw]: # sigmoid
        if r < 0.5:
            res.append(1)
        else:
            res.append(0)
    return res

def saveRes(testY):
    res = []
    with open(TXT_INPUT, mode='r', encoding="utf-8") as fr:
        for i, line in enumerate(fr.readlines()):
            splitline = str(line).strip().split('\t')
            res.append("{0}\t{1}".format(splitline[0], testY[i]))
    with open(TXT_OUTPUT, mode='w', encoding="utf-8") as fw:
        fw.write('\n'.join(res))

if __name__ == "__main__":
    st = time.time()
    word2index = getIdMapWord()
    print("get IdMapWord time: %f s." % (time.time()-st))
    st = time.time()
    testX = getTestX(word2index)
    print("get testX time: %f s." % (time.time()-st))
    st = time.time()
    model = loadModel()
    print("load model time: %f s." % (time.time()-st))
    st = time.time()
    res = predictTestY(model, testX)
    saveRes(res)
    print("predict and save res time: %f s." % (time.time()-st))