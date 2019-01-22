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
TXT_INPUT = r"pre_train.txt"
MODEL_FILE = r"model1.h5"
EMBED_SIZE = 100 # 网络中嵌入层生成的向量的大小
NUM_FILTERS = 128 # 卷积层训练的卷积滤波器的数目
NUM_WORDS = 6 # 每个滤波器的大小，即每次我们将卷积多少个词
BATCH_SIZE = 64 # 每次送入网络的记录的数量
NUM_EPOCHS = 10 # 训练中对整个数据集的所有样例重复运行的次数
MAX_LEN = 0 # 最大的句子长度
VOCAB_SIZE = 0 # 字典的大小，即词个数

def getIdMapWord():
    '''
    根据需要读写文档，将分好词的语料库的词作为字典，并赋予词对应的id
    '''
    if not os.path.exists(PKL_FILE):
        # 统计各个词出现次数
        counter = collections.Counter()        
        maxlen = 0
        with open(TXT_INPUT, mode='r', encoding="utf-8") as fr:
            for line in fr.readlines():
                splitline = str(line).strip().split('\t')
                words = splitline[1].split(' ')
                maxlen = max(len(words), maxlen)
                for word in words:
                    counter[word] += 1
        # 根据出现次数由小到大排序，并分配自增id
        word2index = {}
        counter = sorted(counter.items(), key=lambda item: item[1])
        for wid, word in enumerate(counter):
            word2index[word[0]] = wid + 1 # 因为后期补0处理，所以id不能从0开始编号
        word2index["<OOV>"] = wid + 2 # 未登录词out of vocabulary 
        # 记录全局参数
        word2index["<global_parameter>"] = {
            "MAX_LEN": maxlen,
            "VOCAB_SIZE": len(word2index) + 1
        }
        # 存档
        with open(PKL_FILE, mode="wb") as fw:
            pickle.dump(word2index, fw)
    else:
        with open(PKL_FILE, mode="rb") as fr:
            word2index = pickle.load(fr)
    # 设置全局参数并删除字段
    global MAX_LEN
    MAX_LEN = word2index["<global_parameter>"]["MAX_LEN"]
    global VOCAB_SIZE
    VOCAB_SIZE = word2index["<global_parameter>"]["VOCAB_SIZE"]
    del word2index["<global_parameter>"]
    
    return word2index

def getXandY(word2index):
    '''
    1. 利用字典将输入语句转成id列表
    2. 用0来填充句子，使其达到MAX_LEN，即训练集最长句子的单词数量
    3. 返回训练语句id列表以及对应的标签，格式已经符合模型的输入
    '''
    xs, ys = [], []
    with open(TXT_INPUT, mode='r', encoding="utf-8") as fr:
        for line in fr.readlines():
            splitline = str(line).strip().split('\t')
            ys.append(int(splitline[-1]))
            words = splitline[1].split(' ')
            wid = [word2index[word] for word in words]
            xs.append(wid)
    X = pad_sequences(xs, maxlen=MAX_LEN)
    # Y = np_utils.to_categorical(ys)
    # return X, Y
    return X, ys

def trainAndSaveModel(Xtrain, Ytrain):
    '''
    根据数据与标签已经全局参数训练并存储模型
    '''
    print(MAX_LEN)
    print(VOCAB_SIZE)
    model = Sequential()
    model.add(Embedding(VOCAB_SIZE, EMBED_SIZE, input_length=MAX_LEN))
    model.add(SpatialDropout1D(0.2))
    model.add(Conv1D(filters=NUM_FILTERS, kernel_size=NUM_WORDS, padding="valid", activation="relu"))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(1, activation="sigmoid"))
    # model.add(Dense(2, activation="softmax"))
    # 编译模型，因为目标是二分类，所以选用binary_crossentropy作为我们损失函数
    # 优化器选择adam
    # 之后用训练集训练集模型，批大小设置为 BATCH_SIZE ，训练 NUM_EPOCHS 个周期
    # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.summary()
    model.fit(Xtrain, Ytrain, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS)
    model.save(MODEL_FILE)

if __name__ == "__main__":
    st = time.time()
    word2index = getIdMapWord()
    print("get IdMapWord time: %f s." % (time.time()-st))
    st = time.time()
    trainX, trainY = getXandY(word2index)
    print("get trainX and trainY time: %f s." % (time.time()-st))
    st = time.time()
    trainAndSaveModel(trainX, trainY)
    print("train time: %f min." % ((time.time()-st)/60))