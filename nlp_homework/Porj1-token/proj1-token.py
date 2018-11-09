#!/usr/bin/python3
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
                lineBlocks = str(line).strip().split(self.__splitChar)
                partOfSpeech = [l for l in lineBlocks[1:] if l[-1:] == '.'] # can't '.' in l, because '.' may in Chinese
                self.__dictEnCh[lineBlocks[0]] = partOfSpeech

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

def unregularReduction(d, word):
    flag = False
    if word == 'went': # went -> go (PAST)
        flag = d.showWord("go")
    elif word == "gone": # gone -> go (VEN)
        flag = d.showWord("go")
    elif word == "sat": # sat -> sit (PAST) (VEN)
        flag = d.showWord("sit")
    # can add other rules!
    return flag

def verbJudgeAndReduction(d, word):
    flag = unregularReduction(d, word)
    if not flag:
        flag = d.showWord(word)
    if((not flag) and word[-1:]=='s'): # *s -> * (SINGULAR3)
        flag = d.showWord(word[:-1])
    if((not flag) and word[-2:]=='es'): # *es -> * (SINGULAR3)
    # can't use elif, because the flag may be changed in Previous code block,
    # and previous condition finished Calculating the flag so elif don't calculate again.
        flag = d.showWord(word[:-2])
    if((not flag) and word[-3:]=='ies'): # *ies -> *y (SINGULAR3)
        flag = d.showWord(word[:-3]+'y')
    if((not flag) and word[-3:]=='ing'): # *ing -> * (VING)
        flag = d.showWord(word[:-3])
    if((not flag) and word[-3:]=='ing'): # *ing -> *e (VING)
        flag = d.showWord(word[:-3]+'e')
    if((not flag) and word[-4:]=='ying'): # *ying -> *ie (VING)
        flag = d.showWord(word[:-4]+'ie')
    if((not flag) and word[-3:]=='ing'): # *??ing -> *? (VING)
        flag = d.showWord(word[:-4])
    if((not flag) and word[-2:]=='ed'): # *ed -> * (PAST)(VEN)
        flag = d.showWord(word[:-2])
    if((not flag) and word[-2:]=='ed'): # *ed -> *e (PAST)(VEN)
        flag = d.showWord(word[:-1])
    if((not flag) and word[-3:]=='ied'): # *ied -> *y (PAST)(VEN)
        flag = d.showWord(word[:-3]+'y')
    if((not flag) and word[-2:]=='ed'): # *??ed -> *? (PAST)(VEN)
        flag = d.showWord(word[:-3])
    return flag

if __name__ == '__main__':
    d = myDict()
    # d.showDict(10)
    try:
        while True:
            word = input("Input an English word: ")
            if(not verbJudgeAndReduction(d, word)):
                print("Calling unloaded word module!")
    except EOFError: # ctrl+d in unix-like system, ctrl+c in ms-dos
        exit()