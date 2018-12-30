import ast
import sys
import time

# 最长公共子串（Longest-Common-Substring，LCS）
def LCStrRecursive(s1, s2):
    '''
    暴力求解：递归的方法
    '''
    if len(s1) == 0 or len(s2) == 0:
        return 0
    elif s1[0] == s2[0]:
        return LCStrRecursive(s1[1:], s2[1:]) + 1
    else:
        return max(LCStrRecursive(s1[1:], s2), LCStrRecursive(s1, s2[1:]))


def LCStrdp(s1, s2):
    """
    longest common subsequence of s1 and s2
    """
    if len(s1) == 0 or len(s2) == 0:
        return 0
    dp = [ [0 for _ in range(len(s2)+1) ] for _ in range(len(s1)+1)]
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max([dp[i-1][j], dp[i][j-1]])
    return dp[len(s1)][len(s2)]
    # print("length of LCS is : %d" % dp[len(s1)][len(s2)])
    # # 输出最长公共子序列
    # i, j = len(s1), len(s2)
    # LCS = ""
    # while i > 0 and j > 0:
    #     # 这里一定要比较a[i-1]和b[j-1]是否相等
    #     if s1[i-1] == s2[j-1] and dp[i][j] == dp[i-1][j-1] + 1:
    #         LCS = s1[i-1] + LCS
    #         i, j = i-1, j-1
    #     elif dp[i][j] == dp[i-1][j]:
    #         i, j = i-1, j
    #     elif dp[i][j] == dp[i][j-1]:
    #         i, j = i, j-1
    # print("LCS is : " + LCS)

# 编辑距离
def EditDistance(word1, word2):
    word1 = ' ' + word1
    word2 = ' ' + word2
    target = [['' for _ in range(len(word2))] for _ in range(len(word1))]
    for i in range(len(word1)):
        target[i][0] = i
    for j in range(len(word2)):
        target[0][j] = j
    for i in range(1, len(word1)):
        for j in range(1, len(word2)):
            if word1[i] != word2[j]:
                target[i][j] = min(target[i-1][j] + 1, target[i][j-1] + 1, target[i-1][j-1] + 1)
            else:
                target[i][j] = min(target[i-1][j] + 1, target[i][j-1] + 1, target[i-1][j-1])
            # print('target[%d][%d]'%(i, j),target[i][j])
    return target[len(word1) - 1][len(word2) - 1]

# 最长公共子序列 (The Longest Common Subsequence)
def LCSeq(s1, s2): 
    # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果
    m = [ [ 0 for _ in range(len(s2)+1) ] for _ in range(len(s1)+1) ] 
    # d用来记录转移方向
    d = [ [ None for _ in range(len(s2)+1) ] for _ in range(len(s1)+1) ] 
    ok, left, up = 0, -1, 1
    for p1 in range(len(s1)): 
        for p2 in range(len(s2)): 
            if s1[p1] == s2[p2]:            # 字符匹配成功，则该位置的值为左上方的值加1
                m[p1+1][p2+1] = m[p1][p2]+1
                d[p1+1][p2+1] = ok
            elif m[p1+1][p2] > m[p1][p2+1]:  # 左值大于上值，则该位置的值为左值，并标记回溯时的方向
                m[p1+1][p2+1] = m[p1+1][p2] 
                d[p1+1][p2+1] = left
            else:                           # 上值大于左值，则该位置的值为上值，并标记方向up
                m[p1+1][p2+1] = m[p1][p2+1]   
                d[p1+1][p2+1] = up      
    p1, p2 = len(s1), len(s2)
    s = [] 
    while m[p1][p2]:    # 不为None时
        c = d[p1][p2]
        if c == ok:   # 匹配成功，插入该字符，并向左上角找下一个
            s.append(s1[p1-1])
            p1-=1
            p2-=1 
        elif c == left:  # 根据标记，向左找下一个
            p2 -= 1
        elif c == up:   # 根据标记，向上找下一个
            p1 -= 1
    # s.reverse() 
    return(len(s))

def simED(s, t):
    return 1 - 2 * EditDistance(s, t) / ( len(s) + len(t) )

def simLCStr(s, t):
    return 2 * LCStrdp(s, t) / ( len(s) + len(t) )

def simLCSeq(s, t):
    return 2 * LCSeq(s, t) / ( len(s) + len(t) )

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("please input the pyfilename1 and pyfilename2!")
        print("like: python3 astsim.py a.py b.py")
    else:
        filename1 = str(sys.argv[-2])
        filename2 = str(sys.argv[-1])
        print("read file and generate ast......")
        start = time.time()
        with open(filename1, mode="r", encoding="utf-8") as f1:
            file1 = f1.read()
            ast1 = ast.dump(ast.parse(file1))

        with open(filename2, mode="r", encoding="utf-8") as f2:
            file2 = f2.read()
            ast2 = ast.dump(ast.parse(file2))
        print("    running time: " + str(time.time()-start))

        print("calculate sim with Edit Distance")
        start = time.time()
        s1 = simED(ast1, ast2)
        print("  sim with ED is %f" % s1)
        print("    running time: " + str(time.time()-start))

        print("calculate sim with Longest Common Substring")
        start = time.time()
        s2 = simLCStr(ast1, ast2)
        print("  sim with LCStr is %f" % s2)
        print("    running time: " + str(time.time()-start))
            
        print("calculate sim with Longest Common Subsequence")
        start = time.time()
        s3 = simLCSeq(ast1, ast2)
        print("  sim with LCSeq is %f" % s3)
        print("    running time: " + str(time.time()-start))

        print("相似度为: %f" % (sum([s1, s2, s3])/3) )