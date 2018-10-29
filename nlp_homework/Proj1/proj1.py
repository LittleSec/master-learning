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

def verbJudgeAndReduction(d, word):
    flag = d.showWord(word)
    if((not flag) and word[-1:]=='s'):
        flag = d.showWord(word[:-1])
    if((not flag) and word[-2:]=='es'): 
    # can't use elif, because the flag may be changed in Previous code block,
    # and previous condition finished Calculating the flag so elif don't calculate again.
        flag = d.showWord(word[:-2])
    if((not flag) and word[-3:]=='ies'):
        flag = d.showWord(word[:-3]+'y')
    if((not flag) and word[-3:]=='ing'):
        flag = d.showWord(word[:-3])
    if((not flag) and word[-3:]=='ing'):
        flag = d.showWord(word[:-3]+'e')
    if((not flag) and word[-4:]=='ying'):
        flag = d.showWord(word[:-4]+'ie')
    if((not flag) and word[-3:]=='ing'):
        flag = d.showWord(word[:-4])
    if((not flag) and word[-2:]=='ed'):
        flag = d.showWord(word[:-2])
    if((not flag) and word[-2:]=='ed'):
        flag = d.showWord(word[:-1])
    if((not flag) and word[-3:]=='ied'):
        flag = d.showWord(word[:-3]+'y')
    if((not flag) and word[-2:]=='ed'):
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