import requests
import urllib3
import itertools

# Helper Functions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getCiphertext(plaintext):
    headers = {'Content-Type': 'text/plain'}
    data = '{"plaintext":"%s","password":"3fc52325906d9d51bb208bf28986df7f","teamname":"team58"}' % plaintext                                                           
    response = requests.post('https://172.27.26.181:9997/eaeae', headers=headers, data=data, verify=False)
    return response.json()['ciphertext']

def convertToByteFormat(i):
    first_digit = chr(ord('f') + (i % 16))
    second_digit = chr(ord('f') + (i // 16))
    return second_digit + first_digit

def convertToIntgerFormat(byte):
    second = ord(byte[0]) - ord('f')
    first = ord(byte[1]) - ord('f')
    return (second*16)+first


# Breaking password functions
def getNextPlaintextByte(known_bytes_pos, byte, known_length):
    
    possibilities = []
    for p in known_bytes_pos[known_length // 2]:
        for i in range(0, 127):
            current_byte = convertToByteFormat(i)
            plaintext = p + current_byte
            result = getCiphertext(plaintext)[known_length:known_length+2]
            if(result == byte):
                possibilities.append(plaintext)

    return possibilities

def break_password(ciphertext):
    
    cipher = [ ciphertext[i:i+2] for i in range(0, 16, 2) ]
    result_pos = [[""]]

    # Get Bytes one by one
    for i in range(8):
        #print(result_pos[i])
        result_pos.append(getNextPlaintextByte(result_pos, cipher[i], i*2))

    print(result_pos[8])
    return result_pos[8]

def shorten(plaintext):

    half_bytes = [ convertToIntgerFormat(plaintext[i:i+2]) for i in range(0, len(plaintext), 2) ]
    characters = [ chr(i) for i in half_bytes]

    print(characters)
    return "".join(characters)


def main():
    password = "ktirlqhtlqijmmhqmgkplijngrluiqlq"
    #password = "fomqkmijkgmhlsjl"
    ciphertexts = [ password[i:i+16] for i in range(0, len(password), 16) ]
    plaintexts = [ break_password(i) for i in ciphertexts ]
    results = []
    for i in itertools.product(*plaintexts):
        results.append("".join(i))
    final_results = [ shorten(c) for c in results ]
    for i in final_results:
        print(final_results)


main()
