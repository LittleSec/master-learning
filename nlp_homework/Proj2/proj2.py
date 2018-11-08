#!/usr/bin/python3
class myDict:
    __splitChar = ','
    __fileName = "ce.txt"
    __dictChEn = {}

    def __init__(self, fileName=None):
        if not fileName is None:
            self.__fileName = fileName
        self.__loadDictionary()

    def __loadDictionary(self):
        with open(self.__fileName, encoding='utf-8') as f:
            for line in f.readlines():
                lineBlocks = str(line).strip().split(self.__splitChar)
                self.__dictChEn[lineBlocks[0]] = lineBlocks[1:]

    def isInDict(self, s):
        return s in self.__dictChEn

    def showWord(self, word):
        '''if d is empty or word not in d, then return False, else print and return True'''
        if self.__dictChEn and word in self.__dictChEn:
            print("中文: " + word)
            print("英文: " + str(self.__dictChEn[word]))
            return True
        else:
            return False

    def showDict(self, num=10):
        i = 0
        for k, v in self.__dictChEn.items():
            if i < num:
                print(k, v)
            else:
                break
            i+=1

def FMM(s, d):
    splitRes = []
    i = 0
    while i < len(s):
        for j in range(len(s), i, -1):
            tmp = s[i:j]
            if len(tmp)==1:
                splitRes.append(tmp)
            elif d.isInDict(tmp):
                splitRes.append(tmp)
                i += (len(tmp)-1)
        i+=1
    return splitRes

def RMM(s, d):
    splitRes = []
    i = len(s)
    while i > 0:
        for j in range(len(s)):
            if i <= j:
                break
            tmp = s[j:i]
            if len(tmp)==1:
                splitRes.append(tmp)
            elif d.isInDict(tmp):
                splitRes.append(tmp)
                i -= (len(tmp)-1)
        i-=1
    return splitRes[::-1] # list[start:end;step]

if __name__ == '__main__':
    d = myDict()
    # d.showDict()
    s = '细胞分裂组织'
    print(FMM(s, d))
    print(RMM(s, d))