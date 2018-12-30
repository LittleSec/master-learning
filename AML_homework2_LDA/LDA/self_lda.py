#!/usr/bin python3
# -*- coding:utf-8 -*-
import numpy as np
import random
import os
from collections import OrderedDict
import time

class LDAModel(object):

    def __init__(self, newsInfo, config):

        self.newsInfo = newsInfo  # 获取预处理参数

        # 模型参数
        # 聚类个数K，迭代次数iter_times,每个类特征词个数M,超参数α（alpha） β(beta)
        self.K = config["K"]
        self.beta = config["beta"]
        self.alpha = config["alpha"]
        self.iter_times = config["iter_times"]
        self.M = config["M"]

        self.topNfile = "self_lda_K%dM%d_iter%d" % (self.K, self.M, self.iter_times)
        # p,概率向量 double类型，存储采样的临时变量
        # nw,词word在主题topic上的分布
        # nwsum,每各topic的词的总数
        # nd,每个doc中各个topic的词的总数
        # ndsum,每各doc中词的总数
        self.p = np.zeros(self.K)
        self.nw = np.zeros((self.newsInfo["words_count"], self.K), dtype="int")
        self.nwsum = np.zeros(self.K, dtype="int")
        self.nd = np.zeros((self.newsInfo["docs_count"], self.K), dtype="int")
        self.ndsum = np.zeros(self.newsInfo["docs_count"], dtype="int")
        self.Z = np.array(
            [[0 for y in range(newsInfo["docs"][x]["length"])] for x in range(newsInfo["docs_count"])])        # M*doc.size()，文档中词的主题分布

        # 随机先分配类型
        for x in range(len(self.Z)):
            self.ndsum[x] = self.newsInfo["docs"][x]["length"]
            for y in range(self.newsInfo["docs"][x]["length"]):
                topic = random.randint(0, self.K-1)
                self.Z[x][y] = topic
                self.nw[self.newsInfo["docs"][x]["words"][y]][topic] += 1
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1

        self.theta = np.array(
            [[0.0 for y in range(self.K)] for x in range(self.newsInfo["docs_count"])])
        self.phi = np.array(
            [[0.0 for y in range(self.newsInfo["words_count"])] for x in range(self.K)])

    def sampling(self, i, j):
        topic = self.Z[i][j]
        word = self.newsInfo["docs"][i]["words"][j]
        self.nw[word][topic] -= 1
        self.nd[i][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[i] -= 1

        Vbeta = self.newsInfo["words_count"] * self.beta
        Kalpha = self.K * self.alpha
        self.p = (self.nw[word] + self.beta) / (self.nwsum + Vbeta) * (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)
        for k in range(1, self.K):
            self.p[k] += self.p[k-1]

        u = random.uniform(0, self.p[self.K-1])
        for topic in range(self.K):
            if self.p[topic] > u:
                break

        self.nw[word][topic] += 1
        self.nwsum[topic] += 1
        self.nd[i][topic] += 1
        self.ndsum[i] += 1

        return topic

    def est(self):
        for x in range(self.iter_times):
            for i in range(self.newsInfo["docs_count"]):
                for j in range(self.newsInfo["docs"][i]["length"]):
                    topic = self.sampling(i, j)
                    self.Z[i][j] = topic
        # 迭代完成
        self._theta()  # 计算文章-主题分布
        self._phi()  # 计算词-主题-词分布

        # 保存模型
        self.save()

    def _theta(self):
        for i in range(self.newsInfo["docs_count"]):
            self.theta[i] = (self.nd[i]+self.alpha) / (self.ndsum[i]+self.K * self.alpha)

    def _phi(self):
        for i in range(self.K):
            self.phi[i] = (self.nw.T[i] + self.beta) / (self.nwsum[i]+self.newsInfo["words_count"] * self.beta)

    def save(self):
        # 保存每个主题topic的词
        with open(self.topNfile, mode='w', encoding='utf-8') as f:
            self.M = min(self.M, self.newsInfo["words_count"])
            for i in range(self.K):
                f.write("Topic " + str(i) + ":\n")
                twords = []
                twords = [(n, self.phi[i][n]) for n in range(self.newsInfo["words_count"])]
                twords.sort(key=lambda x: x[1], reverse=True)
                for y in range(self.M):
                    word = OrderedDict({v: k for k, v in self.newsInfo["word2id"].items()})[str(twords[y][0])]
                    f.write('\t\t' + word + ' ' + str(twords[y][1]) + '\n')


def getNewsInfo(wordidfile="wordmapid", trainfile="pre_news.txt"):
    '''
    newsInfo = {}
        docs_count = 0
        words_count = 0
        docs = []
        word2id = {}
    doc = {}
        words = [] # id, not str word
        length = 0
    '''
    newsInfo = {}
    newsInfo["docs"] = []
    word2id = OrderedDict()
    if not os.path.exists(wordidfile):
        print("please preprocess news data at first!")
        return
    with open(wordidfile, mode="r", encoding='utf-8') as fr:
        for l in fr.readlines():
            kv = str(l).strip().split(" ")
            word2id[kv[0]] = kv[1]
        newsInfo["word2id"] = word2id
 
    with open(trainfile, mode='r', encoding='utf-8') as fr:
        for line in fr.readlines():
            if line.strip() != "":
                tmp = line.strip().split(" ")
                doc = {}
                doc["words"] = list(map(lambda x: int(word2id[x]), tmp))
                doc["length"] = len(tmp)
                newsInfo["docs"].append(doc)
            else:
                pass
    newsInfo["docs_count"] = len(newsInfo["docs"])
    newsInfo["words_count"] = len(newsInfo["word2id"])

    return newsInfo


if __name__ == '__main__':
    print("=====获取新闻文档信息=====")
    start = time.time()
    newsInfo = getNewsInfo()
    print("......running time: %f s" % (time.time()-start))
    
    config = {}
    config["alpha"] = 0.1
    config["beta"] = 0.1
    config["iter_times"] = 100
    config["M"] = 10 # 概率最大的 M = 10 个词
    for K in [5, 10, 20]:
        config["K"] = K  # K = {5, 10, 20} 个主题
        print("=====初始化lda模型，K=%d=====" % K)
        start = time.time()
        lda = LDAModel(newsInfo, config)
        print("......running time: %f s" % (time.time()-start))

        print("=====lda主题模型训练，K=%d=====" % K)
        start = time.time()
        lda.est()
        print("......running time: %f s" % (time.time()-start))

