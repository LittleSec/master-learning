# import jieba
import pkuseg
import time
import string
import re

zh_punctuation = "“”，。！？《》【】（）￥…—~·‘’、&；：「|」"
jieba = pkuseg.pkuseg()

def hasZhCn(word):
    for c in word:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False

def isPunctuation(word):
    punctuation = zh_punctuation + string.punctuation
    for c in word:
        if c not in punctuation:
            return False
    return True

def isEng(word):
    '''
    str自带的isalpha()把日韩文也作为alpha
    '''
    letter_list = string.ascii_letters + string.punctuation
    for c in word:
        if c not in letter_list:
            return False
    return True

def isAlNum(word):
    alnum_list = string.ascii_letters + string.punctuation + string.digits
    for c in word:
        if c not in alnum_list:
            return False
    return True

def isDigit(word):
    '''
    自带的函数如"4.1".isdigit()竟然返回False，也是醉了.
    也可以用re库，毕竟try-catch性能不算好
    '''
    try:
        n = eval(word)
    except Exception:
        return False
    else:
        return True

def hasJapKor(word):
    '''
    并不是全部的日韩文，只是大部分的日韩文
    '''
    a = re.search(u"[\uac00-\ud7a3]+", word)
    b = re.search(u"[\uac00-\ud7a3]+", word)
    if a or b:
        return True
    return False

def replaceTokens(tokenList):
    # tokenList = [t for t in tokenList if not t.isspace()] # 对英文分词有点傻
    for i, t in enumerate(tokenList):
        # 顺序不能调
        if hasJapKor(t):
            tokenList[i] = "<OTHER>"
        elif hasZhCn(t):
            continue
        elif isPunctuation(t):
            tokenList[i] = "<PUN>" # 连续同样的英文符号jieba是不会分开的
        # elif t in string.punctuation:
        #     tokenList[i] = "<PUN_E>"
        # elif t in zh_punctuation:
        #     tokenList[i] = "<PUN_C>"
        elif isDigit(t):
            tokenList[i] = "<NUM>"
        elif isEng(t):
            tokenList[i] = "<ENG>"
        elif isAlNum(t):
            tokenList[i] = "<NAE>"
        else:
            tokenList[i] = "<OTHER>"
    # 连续同样的标签则合一
    i = 0
    while i < len(tokenList)-1: # len(tokenList)是动态变化的，不要用for循环
        if tokenList[i] == tokenList[i+1]: # 其实并不仅仅是标签合一，中文也应该如此，重复中文一般就是电话场景，在train里也是通顺的。
        # if tokenList[i][0] == '<' and tokenList[i][-1] == '>' and tokenList[i] == tokenList[i+1]:
            del tokenList[i]
        else:
            i += 1    
    return tokenList

def preprocessfile(filename):
    with open(file=filename, mode='r', encoding="utf-8") as fr:
        wfres = []
        for line in fr.readlines():
            splitline = str(line).strip().split('\t')
            tokens = list(jieba.cut(splitline[1]))
            tokens = replaceTokens(tokens)
            splitline[1] = ' '.join(tokens)
            wfres.append('\t'.join(splitline))
        with open(file="pre_"+filename, mode='w', encoding='utf-8') as fw:
            fw.write('\n'.join(wfres))

# 对标点进行标签化处理不应该统一，例如句号和括号，不应该归为同一个标签。
if __name__ == "__main__":
    st = time.time()
    # preprocessfile("test_v3.txt")
    for filename in ["train.txt", "test_v3.txt", "test_v2.txt"]:
        # 310.5169494152069, 56.232938289642334, 50.807262659072876
        preprocessfile(filename)
        print(time.time()-st)
        st = time.time()
    # tokens = list(jieba.cut("10路模拟量采集,将采样值발음듣기传至DSP并根据越限值判断越限信号通过总线传至DSP；"))
    # tokens = replaceTokens(tokens)
    # print(tokens)