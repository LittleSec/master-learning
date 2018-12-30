#!/usr/bin python3
# -*- coding:utf-8 -*-

import nltk
import string
import os
import time
from collections import OrderedDict

global zh_punctuation
global stopword

zh_punctuation = string.punctuation + \
    "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟–—‘'’‛“”„‟…‧."

stopword = []
with open("stop_words.txt", mode="r", encoding="utf-8") as fr:
    for l in fr.readlines():
        stopword.append(str(l).strip())  # 不能直接让stopword=fr.readlines()，因为会含有\n


def hasNumbers(s):
    return any(c.isdigit() for c in s)


def textProcessing(news):
    '''
    处理一条新闻，去标点符号-->分词-->去停用词-->去带有数字的词
    '''
    news = news.lower()
    # 去标点
    for c in zh_punctuation:
        news = news.replace(c, "")
    wordlist = nltk.word_tokenize(news)  # 分词
    filtered = [w for w in wordlist if not ((w in stopword) or (hasNumbers(w)))]
    return " ".join(filtered)


def newsProcessAndSave(filename="news.txt"):
    if os.path.exists("pre_"+filename):
        return
    with open(filename, mode="r", encoding="utf-8") as fr:
        with open("pre_"+filename, mode="a+", encoding="utf-8") as fa:
            for l in fr.readlines():
                pre_new = textProcessing(str(l).strip())
                fa.write(pre_new + '\n')


def wordMapIdProcessAndSave(filename='pre_news.txt'):
    news = []
    word2id = OrderedDict()
    items_idx = 0
    with open(filename, mode='r', encoding='utf-8') as fr:
        for l in fr.readlines():
            news = str(l).strip()
            if news != "":
                words = news.split(" ")
                for w in words:
                    if not w in word2id:
                        word2id[w] = items_idx
                        items_idx += 1
        with open("wordmapid", mode='w', encoding='utf-8') as fw:
            for word, id in word2id.items():
                fw.write(word + " " + str(id) + "\n")


if __name__ == "__main__":
    print("预处理数据，分词，去标点、停用词、数字等...")
    start = time.time()
    newsProcessAndSave()
    print("......running time: %f s" % (time.time()-start))
    print("=======================================")
    print("生成word-id对应关系（供非调库lda使用）...")
    start = time.time()
    wordMapIdProcessAndSave()
    print("......running time: %f s" % (time.time()-start))