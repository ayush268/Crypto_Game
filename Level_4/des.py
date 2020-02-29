#!/usr/bin/env python

import utils
import constants

class DES:
    def __init__(self, key, nrounds = 16):
        self.nrounds = nrounds
        self.keys = utils.getRoundKeys(key, nrounds)
       
    def expand(self, x):
        return utils.permute(x, constants.expand)
    
    def add_key(self, x, k):
        return utils.xor(x, k)
    
    def sbox(self, x):
        sout = []
        for bid in range(8):
            sin = x[6*bid:6*(bid+1)]
            row = int(sin[0] + sin[5], 2)
            col = int(''.join(sin[1:5]), 2)
            sout += utils.decimal2bin(constants.sBoxes[bid][row][col], 4)
        sout = ''.join(sout)
        return sout
    
    def permute(self, x, perm):
        return utils.permute(x, perm)
        
    def encrypt_or_decrypt(self, plain, keys):
        # Assumes 64 bit input
        plain = utils.permute(plain, constants.ip)
        l, r = plain[:32], plain[32:]
        for i in range(self.nrounds):
            fE = self.expand(r)
            fX = self.add_key(fE, keys[i])
            fS = self.sbox(fX)
            fP = self.permute(fS, constants.perm)
            l, r = r, utils.xor(fP, l)
        cipher = r + l
        cipher = utils.permute(cipher, constants.ipinv)
        return cipher
    
    def encrypt(self, plain):
        return self.encrypt_or_decrypt(plain, self.keys)
    
    def decrypt(self, cipher):
        return self.encrypt_or_decrypt(cipher, self.keys[::-1])
