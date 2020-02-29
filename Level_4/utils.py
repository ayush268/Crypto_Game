#!/usr/bin/env python

import constants

# General Utility Functions

def permute(k, perm, idx = False):
    if idx == True:
        permutted = []
        for p in perm:
            permutted.append(k[p-1])
    else:
        permutted = ""
        for p in perm:
            permutted += k[p-1]
    return permutted

def shift(k, n):
    return k[n:] + k[:n]

def hex2bin(hexa, length):
    x = bin(int(hexa, 16))[2:]
    return "0"*(length - len(x)) + x

def decimal2bin(decimal, length):
    x = bin(decimal)[2:]
    return "0"*(length - len(x)) + x
    
def xor(a,b):
    xor = [ str(int(x)^int(y)) for x,y in zip(a,b)]
    return ''.join(xor)

def split(x, length = 4):
    return [ x[i:min(i+length, len(x))] for i in range(0,len(x), length)]

def IP(x):
    return permute(x, constants.ip)

def FP(x):
    return permute(x, constants.ipinv)

def expand(x):
    return permute(x, constants.expand)

def applySBox(x, box_number):
    row = int(x[0] + x[5], 2)
    col = int(x[1:5], 2)
    sout = decimal2bin(constants.sBoxes[box_number-1][row][col], 4)
    return sout

def P_inverse(x):
    return permute(x, constants.perminv)

def getP():
    chars = ['0', '1','2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    p = ""
    for i in range(16):
        idx = random.randint(0,15)
        p = p + chars[idx]
    return hex2bin(p, 64)


# Text and Binary interconversion

char2bin = {}
bin2char = {}

for i in range(16):
    binary = bin(i).replace("0b","").zfill(4)
    char2bin[chr(ord('f')+i)] = binary
    bin2char[binary] = chr(ord('f')+i)

def bin2text(word):
    text = ""
    for i in range(len(word)//4):
        text += bin2char[word[4*i:4*(i+1)]]
    return text

def text2bin(word):
    res = ''
    for c in word:
        res+=char2bin[c]
    return res


# Key Generation Functions

def getRoundKeys(key, nrounds = 16):
    keys = []
    key56 = permute(key, constants.pc1)
    left, right = key56[:28], key56[28:]
    for i in range(nrounds):
        left = shift(left, constants.shifts[i])
        right = shift(right, constants.shifts[i])
        combined = left + right
        key48 = permute(combined, constants.pc2)
        keys.append(key48)
    return keys

def getRoundKeysIndices(key, nrounds = 16):
    keys = []
    key56 = permute(key, constants.pc1, True)
    left, right = key56[:28], key56[28:]
    for i in range(nrounds):
        left = shift(left, constants.shifts[i])
        right = shift(right, constants.shifts[i])
        combined = left + right
        key48 = permute(combined, constants.pc2, True)
        keys.append(key48)
    return keys
