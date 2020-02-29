#!/usr/bin/python

import random

input_file = open("input.txt","w+")

ip = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

ipinv = [40,8,48,16,56,24,64,32,
         39,7,47,15,55,23,63,31,
         38,6,46,14,54,22,62,30,
         37,5,45,13,53,21,61,29,
         36,4,44,12,52,20,60,28,
         35,3,43,11,51,19,59,27,
         34,2,42,10,50,18,58,26,
         33,1,41,9,49,17,57,25]

def inv_perm(text):
    new_text = list("0"*64)
    for i in range(64):
        new_text[ipinv[i]-1] = text[i]
    
    return ''.join(new_text)

def perm(text):
    new_text = list("0"*64)
    for i in range(64):
        new_text[ip[i]-1] = text[i]
    
    return ''.join(new_text)


def gen_64_bit_num():
    text = ""
    for i in range(64):
        r = random.randint(0,1)
        c = chr(r+ord('0'))
        text += c
    return text


def apply_diff(text):
    new_text = ""
    for i in range(32):
        r = random.randint(0,1)
        c = chr(r+ord('0'))
        new_text += c

    new_text += text[32:64]
    return new_text

def get_decoded(text):
    decoded_text = ""
    for i in range(0,64,4):
        a = text[i:i+4]
        sum = 0
        for j in range(4):
            sum *= 2
            sum += ord(a[j])-ord('0')
        decoded_text += chr(ord('f')+sum)

    return decoded_text

for i in range(2):
    text1 = gen_64_bit_num()
    text2 = apply_diff(text1)

    print(text1[32:])
    print(text2[32:])
    print()
    print(perm(inv_perm(text1))[32:])
    print(perm(inv_perm(text2))[32:])
    print()
    text1 = inv_perm(text1)
    text2 = inv_perm(text2)

    input_file.write(get_decoded(text1))
    input_file.write("\n")

    input_file.write(get_decoded(text2))
    input_file.write("\n")

input_file.close()
