#!/usr/bin python3
# code by hjx, support by Lei Bu, Xuandong Li, teaching Preliminary Introduction to the Theory of Computation in nju

# an example for Cocke–Younger–Kasami algorithm(CYK)

# an example of Context Free Grammar(CFG) in Chomsky Normal Form(CNF)
startSymbol = 'S'
terminals = ['a', 'b']
variables = [startSymbol, 'A', 'B', 'C']
productions = [
    "S -> AB",
    "A -> BC | a",
    "B -> AC | b",
    "C -> a | b"
]

# what CYK algorithm solved: Determines whether a string belongs to a language.
stringw = "ababa"

def preProcProd(prods):
    ret = {}
    for p in prods:
        head, bodys = p.replace(' ', '').split("->")
        if head not in variables:
            print("[-] production({0}) syntax error: head should be a variable.".format(p))
            break
        ret[head] = []
        for body in bodys.split("|"):
            for s in body:
                if s not in terminals + variables:
                    print("[-] production({0}->{1}) syntax error: body should be a string of variables and terminals.".format(p, body))
                    break
            ret[head].append(body)
    # print(ret)
    return ret

# permutation and combination of 2 Sets.
def permAndComb(set1, set2):
    ret = []
    for i in set1:
        for j in set2:
            ret.append("{0}{1}".format(i, j))
    return ret

# ------------- figure 1 -------------
#                               level   step
#             X15                 4      4      X4
#          X14   X25              3      3      X3
#       X13   X24   X35           2      2      X2
#    X12   X23   X34   X45        1      1      X1
# X11   X22   X33   X44   X55     0      0      X0

# We construct an n-by-n triangular array of sets of variables.
# Xij = {variables A | A =>* ai…aj}.
Xnn = []
for i in range(len(stringw), 0, -1):
    tmp = []
    for j in range(i):
        tmp.append(set())
    Xnn.append(tmp)

# ------------- figure 2 -------------
#  4  | X15 |     |     |     | 
# ----+-----+-----+-----+-----+-----  
#  3  | X14 | X25 |     |     |
# ----+-----+-----+-----+-----+-----        
#  2  | X13 | X24 | X35 |     |
# ----+-----+-----+-----+-----+-----  
#  1  | X12 | X23 | X34 | X45 |
# ----+-----+-----+-----+-----+-----  
#  0  | X11 | X22 | X33 | X44 | X55
# ----+-----+-----+-----+-----+-----  
# i/j |  0  |  1  |  2  |  3  |  4  
# transfer equation:
# Xij --> Xnn[j-i][i-1]
# Xnn[i][j] --> X_j+1_i+j+1 

# when we calculate Xpq, once we select Xpj, then the other one must be X_j+1_q
prod_dict = preProcProd(productions)
# X11, X22, X33, X44, X55
for i, s in enumerate(stringw):
    for k, v in prod_dict.items(): # todo: can opt by a dict record which terminal has been calc.
        if s in v:
            Xnn[0][i].add(k)

# X12, X23, X34, X45...
for curlevel in range(1, len(Xnn[0])):
    for i in range(len(Xnn[curlevel-1])-1): # now we calc Xnn[curlevel][i]
        # print("now we calc Xnn[%d][%d]" % (curlevel, i))
        for j in range(curlevel): # now we select Xnn[j][i], by the way, j increase from 0
            # print("select1 Xnn[%d][%d]" % (j, i))
            select1 = Xnn[j][i]
            # print("select2 is Xnn[%d][%d]" % (curlevel-j-1, j+i+1))
            select2 = Xnn[curlevel-j-1][j+i+1] # we can understand by using transfer equations why other selection is that, or by figure 2.
            for s in permAndComb(select1, select2):
                for k, v in prod_dict.items():
                    if s in v:
                        Xnn[curlevel][i].add(k)

def prettyPrintXnn(X):
    max_set_len = max(map(len, [str(i) for j in X for i in j]))
    print_str = []
    for i in range(len(X)):
        pri_str_i = []
        for j in range(len(X[i])):
            pri_str_i.append("X{0}{1}={2:{width}}".format(j+1, i+j+1, str(X[i][j]), width=max_set_len))
        print_str.insert(0, '  '.join(pri_str_i))
    print('\n'.join(print_str))

prettyPrintXnn(Xnn)

if startSymbol in Xnn[len(stringw)-1][0]:
    print("accept!")
else:
    print("reject!")