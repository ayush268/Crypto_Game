#!/usr/bin/env python3

import requests
from string import ascii_lowercase as al

from itertools import permutations
from bs4 import BeautifulSoup

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

    headers = {
        'authority': 'www.guballa.de',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'origin': 'https://www.guballa.de',
        'upgrade-insecure-requests': '1',
        'dnt': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'referer': 'https://www.guballa.de/substitution-solver',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'cookie': 'PHPSESSID=gs09k79bs320bsk9uhps43vpao; _pk_ref.1.103c=%5B%22%22%2C%22%22%2C1580227838%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.1.103c=1; _pk_id.1.103c=1dd3474a2d21d3ee.1579604859.5.1580231182.1580227838.',
    }
    
    data = {
      'button': '',
      'REQUEST_TOKEN': '32DbcQFAIljWUVFB3EKXP-P92t-EIjkb7VXhLk2ID6k',
      'cipher': add_special_characters(new_text, indices, len(text)), 
      'lang': 'en',
      'break': 'Break Cipher'
    }
    
    response = requests.post('https://www.guballa.de/substitution-solver', headers=headers, data=data)
    print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    answer = soup.find_all('textarea')[1].string
    key = soup.find_all('code')[1].string
    return (answer, key)

def decode(key, perm):
    (p, i) = remove_special_chars(code)
    new = apply_perm(p, perm)
    ans = [chr(ord('a')+key.index(i)) for i in new]
    return add_special_characters(ans, i, len(code))

def main():
    n = 5
    perms = get_permutations(n)
    f = open("plaintexts_5.txt", "a")
    for i in perms:
        (res, key) = get_text_after_perm(ciphertext, i)
        ans = decode(key, i)
        f.write(key)
        f.write("\n")
        f.write(res + " => " + ans)
        f.write("\n########################################################\n\n")
    f.close()

main()
