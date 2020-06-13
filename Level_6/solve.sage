#!/bin/sage

# Function to convert english text into corresponding hex notation
def convert_to_hex(text):
    result = '0x'
    for i in text:
        result += hex(ord(i))[2:]

    return result

# Function to convert a number to hex and then its corresponding english text
def convert_to_text(number):
    hex_value = hex(number)[2:]
    length = len(hex_value)
    result = ''
    for i in range(0, length, 2):
        result += chr(eval('0x' + hex_value[i:i+2]))
    return result


# Coppersmith Attack for finding small roots for the equation
# We know part of the initial message and the password,
# using that we will figure out the remaining part of the message
# i.e. the password
def break_rsa(N, e, known_plaintext, password):
    ZmodN = Zmod(N)
    partial = convert_to_hex(known_plaintext)
    number = eval(partial)
    
    print("Hex Form: ", partial)
    print("Number: ", number)
    
    solutions = []
    
    # Using sage libraries to perform the Coppersmith Attack
    # We currently don't know the size of the password,
    # hence we try out all possibilities
    # upto 25 bytes (200 bits) of password.
    for shift in range(1, 200):
        P.<x> = PolynomialRing(ZmodN, implementation='NTL')

        # we shift it by shift amount of bits
        # assuming unknown password is of shift number of bits
        # then we add x which is the variable we have to find
        # and finally we find the value of x by coppersmith algorithm
        m = number << shift
        f = (m + x)**e - password
        res = f.small_roots()
        if res:
            print(m + res[0])
            solutions.append(res[0])
    
    results = [convert_to_text(i) for i in solutions]
    messages = [known_plaintext+i for i in results]
    
    return messages


def main():
    N = 84364443735725034864402554533826279174703893439763343343863260342756678609216895093779263028809246505955647572176682669445270008816481771701417554768871285020442403001649254405058303439906229201909599348669565697534331652019516409514800265887388539283381053937433496994442146419682027649079704982600857517093
    password = 58851190819355714547275899558441715663746139847246075619270745338657007055698378740637742775361768899700888858087050662614318305443064448898026503556757610342938490741361643696285051867260278567896991927351964557374977619644763633229896668511752432222528159214013173319855645351619393871433455550581741643299
    e = 5
    known_plaintext = "This door has RSA encryption with exponent 5 and the password is "

    results = break_rsa(N, e, known_plaintext, password)
    print("\n###############################################################################")
    for i in results:
        print(i, "\n")

main()
