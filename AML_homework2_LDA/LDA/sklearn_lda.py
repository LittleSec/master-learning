#!/usr/bin python3
# -*- coding:utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import time
import os

def saveTopWords(lda_model, feature_name, filename, M=10):
    with open(filename, mode="w", encoding="utf-8") as fw:
        for i, topic in enumerate(lda_model.components_):
            fw.write("Topic " + str(i) + ":\n")
            topMindex = topic.argsort()[:-M-1:-1]
            s = sum(topic)
            for j in topMindex:
                fw.write("\t\t%s %f\n" % (feature_name[j], topic[j]/s))

if __name__ == "__main__":
    newsLst = []
    with open("pre_news.txt", mode="r", encoding="utf-8") as fr:
        for l in fr.readlines():
            newsLst.append(str(l).strip())

    print("=====统计词频并保存=====")
    start = time.time()
    if os.path.exists("tf_vec"):
        with open("tf_vec", mode="rb") as frb:
            tf_vec = pickle.load(frb)
    else:
        tf_vec = CountVectorizer(stop_words='english')
        with open("tf_vec", mode="wb") as fwb:
            pickle.dump(tf_vec, fwb)
    tf = tf_vec.fit_transform(newsLst)
    print("......running time: %f s" % (time.time()-start))
    

    M = 10 # 每个主题下概率最大的M = 10个词
    for K in [5, 10, 20]: # K个主题, K = {5, 10, 20}
        print("=====LDA主题模型训练，K=%d=====" % K)
        start = time.time()
        lda = LatentDirichletAllocation(n_components=K, max_iter=100, learning_method="batch")
        lda.fit(tf)
        filename = "sklearn_lda_K%dM%d_iter%d" % (K, M, 100)
        saveTopWords(lda, tf_vec.get_feature_names(), filename, M)
        print("......running time: %f s" % (time.time()-start))
