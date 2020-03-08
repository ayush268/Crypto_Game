import random
#  the numbers in e are between 1 and 126 ( inclusive)
e  = [random.randint(1, 127) for i in range(8)]
a = [[random.randint(0, 128) for i in range(8)]for j in range(8)]
# transformation is e a e a e
from pyfinite import ffield
import numpy as np
field = ffield.FField(7)
inp = [random.randint(0,127) for i in range(8)]

def add(n1, n2):
    return n1 ^ n2

def multiplyScalar(n1, n2):
    return field.Multiply(n1, n2)

def exponentiation(inp, e):
    out = 0
    if e == 0:
        out = 1
    elif e == 1:
        out = inp
    elif e % 2 == 0:
        sq = exponentiation(inp, int(e/2))
        out = multiplyScalar(sq, sq)
    elif e % 2 == 1:
        sq = exponentiation(inp, int(e/2))
        out1 = multiplyScalar(sq, sq)
        out = multiplyScalar(out1, inp)
    return out
    # pass

def multiplyVectorbyScalar(v, s):
    out = [0] * 8
    for i in range(len(v)):
        out[i] = multiplyScalar(v[i], s)
    return out
def addVectors(v1, v2):
    out = [add(v1[i], v2[i]) for i in range(len(v1))]
    return out

def multiplyMatrixByVector(mat, vec):
    out = [0] * 8
    for row, elem in zip(mat, vec):
        out = addVectors(out, multiplyVectorbyScalar(row, elem))
    return out

def convert2CharToByte(s):
    c1 = s[0]
    c2 = s[1]
    return (ord(c1) - ord('f')) * 16 + (ord(c2) - ord('f'))

def convertStrToByteString(s):
    out = []
    for i in range(0, len(s), 2):
        out += [convert2CharToByte(s[i:i+2])]
    return out

def EAEAE(inp, e, a):
    out = [0 for i in range(8)]
    for i in range(len(inp)):
        out[i] = exponentiation(inp[i], e[i])
    out = multiplyMatrixByVector(a, out)
    for i in range(len(out)):
        out[i] = exponentiation(out[i], e[i])
    out = multiplyMatrixByVector(a, out)
    for i in range(len(out)):
        out[i] = exponentiation(out[i], e[i])
    return out

e = [[] for i in range(8)]
a = [[[] for i in range(8)] for j in range(8)]
inputFile = open("inputs.txt", 'r')
outputFile = open("outputs.txt", 'r')
for ind, (iline, oline) in enumerate(zip(inputFile.readlines(), outputFile.readlines())):
    inputBytes = []
    outputBytes = []
    inputBytes = [convertStrToByteString(i)[ind] for i in iline.strip().split(" ")] 
    outputBytes = [convertStrToByteString(i)[ind] for i in oline.strip().split(" ")] 
    # print(outputBytes)
    for i in range(1, 127):
        for j in range(1, 128):
            flag = True
            for inps, outs in zip(inputBytes, outputBytes):
                if outs != exponentiation(multiplyScalar(exponentiation(multiplyScalar(exponentiation(inps, i), j), i), j), i):
                    flag = False
                    break
            if flag == False:
                continue
            e[ind].append(i)
            a[ind][ind].append(j)
# print(a)
# print(e)



inputFile = open("inputs.txt", 'r')
outputFile = open("outputs.txt", 'r')
for ind, (iline, oline) in enumerate(zip(inputFile.readlines(), outputFile.readlines())):
    if ind > 6 :
        break
    inputBytes = []
    outputBytes = []
    inputBytes = [convertStrToByteString(i)[ind] for i in iline.strip().split(" ")] 
    outputBytes = [convertStrToByteString(i)[ind+1] for i in oline.strip().split(" ")] 
    
    for i in range(1, 128):
        for eiplusone, aiplusoneplusone in zip(e[ind+1], a[ind+1][ind+1]):
            for ei, aii in zip(e[ind], a[ind][ind]):
                flag = True
                for inp, outp in zip(inputBytes, outputBytes):
                    E1 = exponentiation(inp, ei)
                    A1i = multiplyScalar(E1, aii)
                    A1iplusone =  multiplyScalar(E1, i)
                    E2i = exponentiation(A1i, ei)
                    E2iplusone = exponentiation(A1iplusone, eiplusone)
                    A2iplusone = add(multiplyScalar(E2i, i) ,multiplyScalar(E2iplusone, aiplusoneplusone))
                    E3iplusone = exponentiation(A2iplusone, eiplusone)
                    if outp != E3iplusone:
                        flag = False
                        break
                if flag:
                    e[ind+1] = [eiplusone]
                    a[ind+1][ind+1] = [aiplusoneplusone]
                    e[ind] = [ei]
                    a[ind][ind] = [aii]
                    a[ind][ind+1] = [i]

# we have found unique value of e
for i in range(len(e)):
    e[i] = e[i][0]

for diag in range(2, 8):
    exp_list = e
    linTrans = [[0 for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            linTrans[i][j] = 0 if len(a[i][j]) == 0 else a[i][j][0]
    inputFile = open("inputs.txt", 'r')
    outputFile = open("outputs.txt", 'r')
    for ind, (iline, oline) in enumerate(zip(inputFile.readlines(), outputFile.readlines())):
        if ind + diag >= 8:
            break
        inputBytes = [convertStrToByteString(i) for i in iline.strip().split(" ")]
        outputBytes = [convertStrToByteString(i) for i in oline.strip().split(" ")]
        for i in range(1, 128):
            linTrans[ind][ind+diag] = i
            flag = True
            for inps, outs in zip(inputBytes, outputBytes):
                if EAEAE(inps, exp_list, linTrans)[ind+diag] != outs[ind+diag]:
                    flag = False
                    break
            if flag:
                a[ind][ind+diag] = [i]
    inputFile.close();
    outputFile.close();
linTrans = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        linTrans[i][j] = 0 if len(a[i][j]) == 0 else a[i][j][0]
a = np.array(linTrans).T
e = exp_list
print("E and A broken. Key found.")
print("E = ", e)
print("A = ", a)
# print(np.ndarray(a).T)
s = "ktirlqhtlqijmmhqmgkplijngrluiqlq"
password_1 = s[:16]
password_2 = s[16:]

def convertByteto2Char(b):
    binaryrep = format(format(b,"08b"))
    a = chr(int(binaryrep[:4], 2) + ord('f'))
    b = chr(int(binaryrep[4:], 2) + ord('f'))
    return a+b
def decrypt(password):
    passw = convertStrToByteString(password)
    op = ""
    # print(passw)
    for ind in range(8):
        for ans in range(128):
            inp = op + convertByteto2Char(ans)+(16-len(op)-2)*'f'
            if passw[ind] == EAEAE(convertStrToByteString(inp), exp_list, linTrans)[ind]:
                op += convertByteto2Char(ans)
                break
    return op

def convertToNormalString(s):
    out = ""
    for i in range(0, len(s), 2):
        out += chr((ord(s[i]) - ord("f")) * 16 + (ord(s[i+1]) - ord("f")))
    return out
print("password: ",convertToNormalString((decrypt(password_1))+(decrypt(password_2))))