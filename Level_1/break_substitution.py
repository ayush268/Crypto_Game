#!/usr/bin/env python3

from string import ascii_lowercase

count = {}

ciphertext = """Nwy dejp pmcplpz cdp sxlrc adegipl ws cdp aejpr. Er nwy aem rpp cdplp xr mwcdxmv ws xmcplprc xm cdp adegipl. Rwgp ws cdp qecpl adegiplr fxqq ip gwlp xmcplprcxmv cdem cdxr wmp, x eg rplxwyr. Cdp awzp yrpz swl cdxr gprrevp xr e rxgbqp ryircxcycxwm axbdpl xm fdxad zxvxcr dejp ippm rdxscpz in 2 bqeapr. Swl cdxr lwymz berrfwlz xr vxjpm ipqwf, fxcdwyc cdp hywcpr."""

for i in ciphertext:
    if i.lower() in ascii_lowercase:
        if i.lower() in count:
            count[i.lower()] += 1
        else:
            count[i.lower()] = 1

count = {k:v for k,v in reversed(sorted(count.items(), key=lambda item: item[1]))}
print(count)

key = {}
key['p'] = 'e'    # Because 'p' has very high frequency
key['r'] = 's'    # 'r' has very high frequency, _ee word exists, matches with "see" not "bee"
key['i'] = 'b'    # _e word exists, matches with "be"
key['n'] = 'y'    # b_ word exists, matches with "by"
key['m'] = 'n'    # bee_ word exists, matches with "been"
key['w'] = 'o'    # _ne word exists, matches with "one"
key['s'] = 'f'    # o_ word exists, 'n' is already taken, matches with "of"
key['l'] = 'r'    # fo_ word exists, matches with "for"
key['y'] = 'u'    # yo_ word exists, matches with "you"
key['g'] = 'm'    # so_e word exists, matches with "some"
key['z'] = 'd'    # use_ word exists, 'r' is already taken, matches with "used"
key['c'] = 't'    # en_ered word exists, matches with "entered"
key['d'] = 'h'    # t_e word exists, matches with "the"
key['x'] = 'i'    # f_rst word and _ (single letter word) exist, matches with "first" and "i"
key['e'] = 'a'    # single letter word exists, 'i' is already taken, matches with "a"
key['j'] = 'v'    # ha_e word exists, matches with "have"
key['a'] = 'c'    # _hamber word exists, matches with "chamber"
key['v'] = 'g'    # nothin_ word exists, matches with "nothing"
key['f'] = 'w'    # _hich word exists, matches with "which"
key['q'] = 'l'    # be_ow and wi__ word exists, matches with "below" and "will"
key['b'] = 'p'    # sim_le and ci_her word exists, matches with "simple" and "cipher"
key['h'] = 'q'    # _uotes word exists, matches with "quotes"

# For the case of integer digits, "1" must be subtracted from each digit, as mentioned
# text after decryption, it was "2" but it itself was shifted so
# x+x = 2, this gives x = 1

def decrypt(ctext):
    plaintext = ""
    for i in ctext:
        if i.lower() in ascii_lowercase:
            if i.lower() in key:
                if i in ascii_lowercase:
                    plaintext += key[i]
                else:
                    plaintext += chr(ord(key[i.lower()]) - ord('a') + ord('A'))
            else:
                plaintext += i.lower()
        elif i == ' ':
            plaintext += i+i
        elif i.isdigit():
            plaintext += chr(ord(i)-1)
        else:
            plaintext += i

    return plaintext

print(decrypt(ciphertext))

code = "anQp81Qpan"
print(decrypt(code))
