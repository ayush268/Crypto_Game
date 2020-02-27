#!/usr/bin/python

input_file = open("input.txt","r")
output_file = open("output.txt","r")

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

perm = [16,7,20,21,
        29,12,28,17,
        1,15,23,26,
        5,18,31,10,
        2,8,24,14,
        32,27,3,9,
        19,13,30,6,
        22,11,4,25]

perminv = [9,17,23,31,
           13,28,2,18, 
           24,16,30,6, 
           26,20,10,1, 
           8,14,25,3, 
           4,29,11,19, 
           32,12,22,7, 
           5,27,15,21]

expand_key = [32,1,2,3,4,5,
       4,5,6,7,8,9,
       8,9,10,11,12,13,
       12,13,14,15,16,17,
       16,17,18,19,20,21,
       20,21,22,23,24,25,
       24,25,26,27,28,29,
       28,29,30,31,32,1]

s_box = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
      0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
      4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
      15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],

     [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
      3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
      0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
      13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],

     [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
      13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
      13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
      1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],

     [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
      13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
      10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
      3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],

     [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
      14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
      4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
      11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],

     [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
      10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
      9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
      4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],

     [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
      13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
      1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
      6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],

     [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
      1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
      7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
      2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]

def apply_permutation(text,P):
	n = len(P)
	new_text = list("0"*n)
	for i in range(n):
		new_text[i] = text[P[i]-1]
	
	return ''.join(new_text)

def get_coded(text):
	coded_text = ""
	for i in range(0,16):
		x = ord(text[i])-ord('f')
		y = ""
		for j in range(4):
			if x%2==1:
				y+='1'
			else:
				y+='0'
			x = x//2
		coded_text += y[::-1]
	return coded_text

def expand(text):
	new_text = ""
	for i in range(48):
		new_text += text[expand_key[i]-1]
	return new_text

def get_xor(text1, text2):
	new_text = ""
	for i in range(len(text1)):
		new_text += chr(((ord(text1[i])-ord('0'))^(ord(text2[i])-ord('0')))+ord('0'))
	return new_text

def convert(x):
	row = 0
	if x&32 != 0:
		row+=2
	if x&1 != 0:
		row+=1

	col = (x&30)/2
	return row*16+col

Keys = {}

def get_possible_pairs(input1, input2, output_diff, s_box_no):
	input1_value = 0
	input2_value = 0
	output_value = 0

	for i in range(6):
		input1_value *= 2
		input1_value += (ord(input1[i])-ord('0'))

		input2_value *= 2
		input2_value += (ord(input2[i])-ord('0'))

	for i in range(4):
		output_value *= 2
		output_value += (ord(output_diff[i])-ord('0'))

	input_value = input1_value^input2_value

	for input1_after_xor in range(64):
		input2_after_xor = input1_after_xor^input_value

		if (s_box[s_box_no][convert(input1_after_xor)])^(s_box[s_box_no][convert(input2_after_xor)]) == output_value:
			key = (s_box_no,input1_value^input1_after_xor)
			print(key)
			if key in Keys:
				Keys[key] += 1
			else:
				Keys[key] = 1

def solve(in1, in2, out1, out2):
	
	in1 = apply_permutation(in1,ip)
	in2 = apply_permutation(in2,ip)

	out1 = apply_permutation(out1,ipinv)
	out2 = apply_permutation(out2,ipinv)

	L0_1 = in1[0:32]
	L0_2 = in2[0:32]

	L0_diff = get_xor(L0_1, L0_2)
	R1_diff = L0_diff

	L2_diff = R1_diff

	R2_1 = out1[0:32]
	R2_2 = out2[0:32]

	R2_exp_1 = expand(R2_1)
	R2_exp_2 = expand(R2_2)

	R3_1 = out1[32:64]
	R3_2 = out2[32:64]

	R3_diff = get_xor(R3_1,R3_2)
	R3_afterP_diff = get_xor(R3_diff, L2_diff)
	R3_afterS_diff = apply_permutation(R3_afterP_diff,perminv)

	for i in range(1):
		get_possible_pairs(R2_exp_1[(6*i):(6*i+6)], R2_exp_2[(6*i):(6*i+6)], R3_afterS_diff[(4*i):(4*i+4)], i)
		
for i in range(2):
	in1 = input_file.readline().strip()
	in2 = input_file.readline().strip()
	in1_coded = get_coded(in1)
	in2_coded = get_coded(in2)

	out1 = output_file.readline().strip()
	out2 = output_file.readline().strip()
	out1_coded = get_coded(out1)
	out2_coded = get_coded(out2)
	solve(in1_coded, in2_coded, out1_coded,out2_coded)
	print("--------------------------------------------------------------------")
print(Keys)
