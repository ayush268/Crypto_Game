#!/usr/bin/env python

import random
import numpy as np
import utils
from des import DES

def solve_round3(in1, in2, ciphers):
    round3_key = ["0"]*8
    kset = []
    for i in range(8):
        all64 = {}
        for i in range(64):
            all64[i] = 0
        kset.append(all64)

    for i, p in enumerate(in1):
        p1, p2 = p, in2[i]
        x, y = ciphers[p1], ciphers[p2]
        x, y = utils.text2bin(x), utils.text2bin(y)
        x, y = utils.IP(x), utils.IP(y)
        
        cx, cy = x[32:], y[32:]
        Ecx, Ecy = utils.expand(cx), utils.expand(cy)
        lx, ly = x[:32], y[:32]

        l_ = utils.xor(lx, ly)
        p1, p2 = utils.IP(utils.text2bin(p))[:32], utils.IP(utils.text2bin(in2[i]))[:32]
        C_ = utils.xor(utils.xor(p1,p2), l_)
        SOC = utils.P_inverse(C_)

        for bnum in range(1,9,1):
            for i in range(64):
                k = utils.decimal2bin(i, 6)
                SOcx = utils.applySBox(utils.xor(Ecx[6*(bnum-1):6*(bnum)], k), bnum)
                SOcy = utils.applySBox(utils.xor(Ecy[6*(bnum-1):6*(bnum)], k), bnum)
                if utils.xor(SOcx, SOcy) == SOC[4*(bnum-1):4*(bnum)]:
                    kset[bnum-1][i] += 1


    for i, k in enumerate(kset):
        Keymax = max(k, key=k.get)
        round3_key[i] = Keymax
        #print(Keymax, k[Keymax])

    return round3_key

def get_remaining_key_bits(key, k, in1, ciphertexts):
    
    # fill up right indexs
    s = [str(i) for i in range(64)]
    idxs = utils.getRoundKeysIndices(s)[2]

    rem = set()
    for i in range(64):
        rem.add(i)

    i = -1
    key_guess = ['x']*64
    for j, idx in enumerate(idxs):
        i += 1
        idx = int(idx)
        key_guess[idx] = k[i]
        rem.remove(idx)

    for i in range(7, 64, 8):
        rem.remove(i)

    rem = list(rem)
    key_guess = ''.join(key_guess)
    
    # brute force on remaining 14 bits
    for i in range(2**8):
        rem_str = utils.decimal2bin(i, 8)

        j = 0
        key_guess = list(key_guess)
        for r in rem:
            key_guess[r] = rem_str[j]
            j += 1
        key_guess = ''.join(key_guess)

        des_ours = DES(key_guess, 3)

        if des_ours.encrypt(utils.text2bin(in1[5])) == utils.text2bin(ciphertexts[in1[5]]):
            print("Remaining bits =>", i)
            break
    
    return key_guess


def break_des(in_file1, in_file2, out_file1, out_file2, ciphertext):
    input1 = np.load(in_file1)
    input2 = np.load(in_file2)
    
    cipher1 = np.load(out_file1)
    cipher2 = np.load(out_file2)
    
    ciphertexts = {}
    for i, inp in enumerate(input1):
        ciphertexts[inp] = cipher1[i]
    
    for i, inp in enumerate(input2):
        ciphertexts[inp] = cipher2[i]
    
    round3_key = solve_round3(input1, input2, ciphertexts)
    print("Round 3 Key =>", round3_key)
    
    dummy_key = "0000000000000000000000000000000000000000000000000000000000000000"
    keys= utils.getRoundKeys(dummy_key)
    
    k3 = ''.join([utils.decimal2bin(k, 6) for k in round3_key])
    key_guess = get_remaining_key_bits(dummy_key, k3, input1, ciphertexts)
    
    key_guess = key_guess.replace('x', '0')
    print("Final Key =>", key_guess)
    
    # Final Password decryption
    
    des = DES(key_guess, 3)
    password = des.decrypt(utils.text2bin(ciphertext[:16])) + des.decrypt(utils.text2bin(ciphertext[16:]))
    password = utils.bin2text(password)
    print("Decrypted Password =>", password)

# Main

def main():
    # Running break_des
    password = "gnushmilfrplulktkrtrogltjojfqjpt"
    input1 = "in1.npy"
    input2 = "in2.npy"
    cipher1 = "cipher1.npy"
    cipher2 = "cipher2.npy"
    break_des(input1, input2, cipher1, cipher2, password)

main()
