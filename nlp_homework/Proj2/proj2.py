class myDict:
    __splitChar = ' '
    __fileName = "dic_ec.txt"
    __dictEnCh = {}

    def __init__(self, fileName=None):
        if not fileName is None:
            self.__fileName = fileName
        self.__loadDictionary()

    def __loadDictionary(self):
        with open(self.__fileName, encoding='utf-8') as f:
            for line in f.readlines():
                partOfSpeech = []
                lineBlocks = str(line).strip().split(self.__splitChar)
                for l in lineBlocks[1:]:
                    if '.' in l:
                        partOfSpeech.append(l)
                self.__dictEnCh[lineBlocks[0]] = partOfSpeech

    def isInDict(self, s):
        return s in self.__dictEnCh

    def showWord(self, word):
        '''if d is empty or word not in d, then return False, else print and return True'''
        if self.__dictEnCh and word in self.__dictEnCh:
            print("Original from: " + word)
            print("Part of speech: " + str(self.__dictEnCh[word]))
            return True
        else:
            return False

    def showDict(self, num=10):
        i = 0
        for k, v in self.__dictEnCh.items():
            if i < num:
                print(k, v)
            else:
                break
            i+=1


def FMM(s, d):
    splitRes = []
    while i < len(s):
        for j in range(len(s), i, -1):
            tmp = s[i:j]
            if len(tmp)==1:
                splitRes.append(tmp)
            elif d.isInDict(s):
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
            elif d.isInDict(s):
                splitRes.append(tmp)
                i -= (len(tmp)-1)
        i-=1
    return splitRes.reverse()