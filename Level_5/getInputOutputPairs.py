import numpy as np
import json
import requests
m = {}
for i in range(16):
    num = format(i,"04b")
    numi = int(num[3]) + 2 *int(num[2]) + int(num[1]) * 4 + int(num[0])*8
    m[num] = chr(ord('f')+numi)

file = open("inputs.txt","w")
outFile = open("outputs.txt", "w")
for i in range(8):
    for j in range(128):
        binar = np.binary_repr(j, width=8)
        strr = 'ff'*i + m[binar[:4]] + m[binar[4:]] + 'ff'*(8-i-1)
        file.write(strr)
        # data = {"teamname":"codeBusters", "password":"83783eb691ab43f57872603f559db22e", "plaintext": strr}
        data = {"teamname":"team58", "password":"3fc52325906d9d51bb208bf28986df7f", "plaintext": strr}

        response = requests.post('https://172.27.26.181:9999/eaeae', json=data, verify=False)
        ciphertext = json.loads(response.text)["ciphertext"]
        outFile.write(ciphertext)
        file.write(" ")
        outFile.write(" ")
    file.write("\n")
    outFile.write("\n")
file.close()
outFile.close()