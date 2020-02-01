#!/usr/bin/env python3

import requests
import random
from string import ascii_lowercase as al
from itertools import permutations
import enchant

from ngram_score import ngram_score
fitness = ngram_score('quadgrams.txt')

ciphertext = """cpiftgt ef oldo ukuq vtyp vv ptttqkk dp txe tkcnmbi uxkfft ueukwuqe ad uwv ttdo. da tocwc, qqc qgcu woyg cx cpifteud wat tvkbd vu owk zelc dp txe vthr uccfgg. keb dteuof ut gle dzcc rtc wv ukkyyc xxuo edw. mqgu zec dtyac uldw cqev evyu xvo tee moo mt gle dkcur. tm evyoi qtzc cxz o mlcuauoc, vw wetd kkcc gwhego! cf da foedokm, aibet ccd ktbfkqyo:"""
code = "uhs_xafmf_no"

def get_permutations(size):
    perm = permutations(range(size))
    return list(perm)

def remove_special_chars(text):
    ret = ""
    count = 0
    indices = {}
    for i in text:
        if(i.lower() in al):
            ret += i
        else:
            indices[count] = i
        count += 1
    
    return (ret, indices)

def permute(text, perm):
    res = ""
    for i in perm:
        res += text[i]
    return res

def apply_perm(text, perm):
    length = len(perm)
    res = ""
    for i in range(len(text)//length):
        ite = i*length
        res += permute(text[ite:ite+length], perm)
    return res

def add_special_characters(text, indices, size):
    res = ""
    count = 0
    counttext = 0
    for i in range(size):
        if count in indices:
            res += indices[count]
        else:
            res += text[counttext]
            counttext += 1
        count += 1
    return res

def get_text_after_perm(text, perm):
    (plain, indices) = remove_special_chars(text)
    new_text = apply_perm(plain, perm)
    return (new_text, indices)

def substitution_cipher(text):
    maxkey = list('abcdefghijklmnopqrstuvwxyz')
    maxscore = -900000000
    parentkey = maxkey[:]

    answer = ""
    key = ""
    i = 0
    while i<20:
        i = i+1
        parentscore = -900000000
        random.shuffle(parentkey)
        count = 0
        while count < 1000:
            a = random.randint(0,25)
            b = random.randint(0,25)
            child = parentkey[:]
            child[a],child[b] = child[b],child[a]

            deciphered = ""
            for x in text:
                deciphered += chr(ord('A')+child.index(x))
            
            score = fitness.score(deciphered)

            if score > parentscore:
                parentscore = score
                parentkey = child[:]
                count = 0
            count = count+1

        if parentscore>maxscore:
            maxscore,maxkey = parentscore,parentkey[:]
            key = maxkey
            answer = ""
            for x in text:
                answer += chr(ord('A')+maxkey.index(x))

    key_string = "" 
    for x in key: 
        key_string += x
    return (answer, key_string)  

def decode(key, perm):
    (p, i) = remove_special_chars(code)
    new = apply_perm(p, perm)
    ans = [chr(ord('a')+key.index(j)) for j in new]
    return add_special_characters(ans, i, len(code))

def valid_word_count(text):
    d = enchant.Dict("en_US")
    cnt = 0
    cur = ""
    for c in text:
        if c.lower() in al:
            cur += c
        elif cur != "":
            if d.check(cur):
                cnt += 1
            cur = ""
    return cnt

def main():
    n = 5
    perms = get_permutations(n)
    max_valid_words = 0
    ans_text = ""
    ans_code = ""
    ans_key = ""
    
    for i in perms:
        (permuted_text, indices) = get_text_after_perm(ciphertext, i)
        (substituted_text, key) = substitution_cipher(permuted_text)
        res = add_special_characters(substituted_text, indices, len(ciphertext))

        decoded_code = decode(key, i)
        
        if valid_word_count(res) > max_valid_words:
            max_valid_words = valid_word_count(res)
            ans_text = res
            ans_code = decoded_code
            ans_key = key

    print(ans_code)

main()
