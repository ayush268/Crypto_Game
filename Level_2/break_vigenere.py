#!/usr/bin/env python3

from collections import Counter
from string import ascii_lowercase, ascii_uppercase
import operator

def index_of_coincidence(ctext):
    num = 0.0
    den = 0.0
    for val in Counter(ctext).values():
        i = val
        num += i * (i - 1)
        den += i
    if den == 0.0:
        return 0.0
    else:
        return num / (den * (den - 1))

def partition(text, num):
    cols = [""] * num
    for i, c in enumerate(text):
        cols[i % num] += c
    return cols

def find_keylen(ctext, low=3, high=10, rows=5):
    if high > len(ctext) / 2:
        high = len(ctext) / 2

    results = {}
    for length in range(low, high + 1):
        indices = [index_of_coincidence(col) for col in partition(ctext, length)]
        results[length] = sum(indices) / len(indices)

    best = sorted(results.items(), key=lambda kv: -kv[1])

    return [i[0] for i in best]

def freq_score(text):
    freqs = {
        'a': 8167,
        'b': 1492,
        'c': 2782,
        'd': 4253,
        'e': 12702,
        'f': 2228,
        'g': 2015,
        'h': 6094,
        'i': 6966,
        'j': 153,
        'k': 772,
        'l': 4025,
        'm': 2406,
        'n': 6749,
        'o': 7507,
        'p': 1929,
        'q': 95,
        'r': 5987,
        's': 6327,
        't': 9056,
        'u': 2758,
        'v': 978,
        'w': 2360,
        'x': 150,
        'y': 1974,
        'z': 74
    }

    score = 0
    for c in text:
        if c == ' ':
            score += 10000
        elif c.lower() in freqs:
            score += freqs[c.lower()]
        elif ord(c) >= 128:
            score -= 5000
        else:
            score -= 1000

    return score

def find_key(ctext, keylen):
    key = ""
    for col in partition(ctext, keylen):
        scores = {}
        for i, letter in enumerate(ascii_lowercase):
            transposed = [ascii_lowercase[(ascii_lowercase.index(c.lower()) - i) %
                               len(ascii_lowercase)] for c in col]
            scores[letter] = freq_score(transposed)
        key += max(scores.items(), key=operator.itemgetter(1))[0]

    return key

def decrypt(ctext, key):
    rotation_key = [(ord(i) - ord('a')) for i in key]
    keylen = len(rotation_key)

    plaintext = ""
    index = 0
    for c in ctext:
        if c in ascii_lowercase:
           realc = chr((ord(c)-ord('a')-rotation_key[index%keylen]) % 26 + ord('a'))
           plaintext += realc
           index += 1
        elif c in ascii_uppercase:
           realc = chr((ord(c)-ord('A')-rotation_key[index%keylen]) % 26 + ord('A'))
           plaintext += realc
           index += 1
        else:
           plaintext += c

    return plaintext


def remove_special_characters(text):
    filteredtext = ""
    for i in text:
        if i.lower() in ascii_lowercase:
            filteredtext += i.upper()

    return filteredtext


if __name__ == "__main__":

    inputtext = """Lg ccud qh urg tgay ejbwdkt, wmgtf su bgud nkudnk lrd vjfbg. Yrhfm qvd vng sfuuxytj "vkj_ecwo_ogp_ej_rnfkukf" wt iq urtuwjm. Ocz iqa jdag vio uzthsivi pqx vkj pgyd encpggt. Uy hopg yjg fhkz arz hkscv ckoq pgfn vu wwygt nkioe zttft djkth."""

    ciphertext = remove_special_characters(inputtext)

    best_key_lengths = find_keylen(ciphertext)
    #print(best_key_lengths)

    for key_len in best_key_lengths:
        key = find_key(ciphertext, key_len)
        print(key)
        print(decrypt(inputtext, key))

        print("")
