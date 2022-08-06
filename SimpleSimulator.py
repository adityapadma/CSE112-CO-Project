# import matplotlib.pyplot as plt

regval={"000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":0}

flags =["0"]*16

opcode = {
"A" : {"add" : "10000" , "sub" : "10001" , "mul" : "10110" , "xor" : "11010" , "and" : "11100", "or":"11011" , "addf" : "00000" , "subf" : "00001"}, 
"B" : {"mov" : "10010" , "ls" : "11001","rs":"11000" , "movf" : "00010"}, 
"C" : {"mov" : "10011"  ,"div" : "10111" , "not" : "11101" , "cmp" : "11110"},
"D" : {"ld" : "10100" , "st" : "10101"},
"E" : {"jmp" : "11111" , "jlt" : "01100" , "jgt" : "01101" , "je" : "01111"},
"F" : {"hlt" : "01010"} 
}

def binaryToDecimal(binaryValue , check = 0):
    if(check == 1):
        exponent = binaryToDecimal(binaryValue[0:3])
        c = 0
        for i in range(3,8) :
            c += int(binaryValue[i])*(2**(2-i))
        c+=1
        c = c * (2**exponent)
        return c
    decimalValue = 0
    placeValue = 1
    for digit in binaryValue[::-1]:
        decimalValue += (int)(digit) * placeValue
        placeValue *=2
    return decimalValue

def binaryConv(k):
    exponent = 0
    s="00000000"
    if type(k) == float:
        while(k / 2 > 1) :
            exponent += 1
            k = k / 2
        x = k - int(k)
        s += format(exponent,'03b')
        while(x - int(x) !=0) :
            x *= 2
            s += str(int(x))
            x= x - int(x)
        for i in range(16-len(s)):
            s += '0'
        return s
    else:
        return format(k, '016b')


def typeA(opc,reg1,reg2,reg3):
    global flags
    if opc == opcode["A"]["add"]:
        if regval[reg1] + regval[reg2] > 2**16-1:
            regval[reg3] = (regval[reg1] + regval[reg2]) % (2**16)
            if flags[-4] != "1":
                flags[-4] = "1"
        else:
            regval[reg3] = regval[reg1] + regval[reg2]
    elif opc == opcode["A"]["sub"]:
        if(regval[reg1] - regval[reg2]) < 0 :
            regval[reg3] = 0
            if flags[-4] != "1":
                flags[-4] = "1"
        else:
            regval[reg3] = regval[reg1] - regval[reg2]
    elif opc == opcode["A"]["mul"]:
        if regval[reg1] * regval[reg2] > 2**16-1:
            regval[reg3] = (regval[reg1] * regval[reg2]) % (2**16)
            if flags[-4] != "1":
                flags[-4] = "1"
        else:
            regval[reg3] = regval[reg1] * regval[reg2]
    elif opc == opcode["A"]["xor"]:
        regval[reg3] = regval[reg1] ^ regval[reg2]
    elif opc == opcode["A"]["and"]:
        regval[reg3] = regval[reg1] & regval[reg2]
    elif opc == opcode["A"]["or"]:
        regval[reg3] = regval[reg1] | regval[reg2]
    elif opc == opcode["A"]["addf"]:
        x = regval[reg1] + regval[reg2] 
        if x > 252:
            if flags[-4] != "1":
                flags[-4] = "1"
            regval[reg3] = binaryToDecimal("0000000011111111")
        else:
            regval[reg3] = x
    elif opc == opcode["A"]["subf"]:
        x = regval[reg1] - regval[reg2]
        if(x<0):
            if flags[-4] != "1":
                flags[-4] = "1"
            regval[reg3] = binaryToDecimal("0000000000000000")
        else:
            regval[reg3] = x
            
    

def typeB(opc,reg1,imm):
    if opc == opcode["B"]["mov"]:
        imm = binaryToDecimal(imm)
        regval[reg1] = imm
    elif opc == opcode["B"]["ls"]:
        imm = binaryToDecimal(imm)
        regval[reg1] = regval[reg1] * (2**imm)
    elif opc == opcode["B"]["rs"]:
        imm = binaryToDecimal(imm)
        regval[reg1] = regval[reg1] // (2**imm)
    else:
        imm = binaryToDecimal(imm , 1)
        regval[reg1]  = imm                               

def typeC(opc,reg1,reg2):
    global flags
    if opc == opcode["C"]["mov"]:
        if reg1 == "111":
            s=""
            regval[reg2] = binaryToDecimal(s.join(flags))
            flags =["0"]*16
        else:
            regval[reg2] = regval[reg1]
            flags =["0"]*16
    elif opc == opcode["C"]["div"]:
        regval["000"] = regval[reg1] // regval[reg2]
        regval["001"] = regval[reg1] % regval[reg2]
        flags =["0"]*16
    elif opc == opcode["C"]["not"]:
        regval[reg2] = (regval[reg1]) ^ (2**16-1)
        flags =["0"]*16
    elif opc == opcode["C"]["cmp"]:
        flags =["0"]*16
        if regval[reg1] < regval[reg2]:
            if flags[-3] != "1":
                flags[-3] = "1"
        elif regval[reg1] > regval[reg2]:
            if flags[-2] != "1":
                flags[-2] = "1"
        elif regval[reg1] == regval[reg2]:
            if flags[-1] != "1":
                flags[-1] = "1"

def typeD(opc,reg1,mem_addr):
    if opc == opcode["D"]["ld"]:

        regval[reg1] = binaryToDecimal(memory[binaryToDecimal(mem_addr)])
    elif opc == opcode["D"]["st"]:
        memory[binaryToDecimal(mem_addr)] = binaryConv(regval[reg1])

def typeE(opc,mem_addr):
    global flags
    global pc
    if opc == opcode["E"]["jmp"]:
        flags =["0"]*16
        printt()
        pc = binaryToDecimal(mem_addr)
        return 0
    
    elif opc == opcode["E"]["jlt"]:
        if flags[-3] == '1':
            flags =["0"]*16
            printt()
            pc = binaryToDecimal(mem_addr)
        else:
            return -1
    elif opc == opcode["E"]["jgt"]:
        if flags[-2] == '1':
            flags =["0"]*16
            printt()
            pc = binaryToDecimal(mem_addr)
        else:
            return -1
    elif opc == opcode["E"]["je"]:
        if flags[-1] == '1':
            flags =["0"]*16
            printt()
            pc = binaryToDecimal(mem_addr)
        else:
            return -1

import sys

inst0=sys.stdin.read().splitlines()

inst = [ i for i in inst0 if i!=""]

pc = 0
memory = [ "0" * 16 ] * 256

for i in range(len(inst)):
    memory[i]=inst[i]

def printt():
    global flags
    print(format(pc, '08b'), end = " ")
    s=""
    for i in regval:
        if i!="111":
            print(binaryConv(regval[i]),end=" ")
    print(s.join(flags))

cycle=0

while(inst[pc]!="0101000000000000"):
    comm=inst[pc]
    # plt.plot(cycle,pc,'bo')
    opc = comm[:5]
    if opc in opcode["A"].values():
        flags =["0"]*16
        typeA( opc , comm[7:10] , comm[10:13] , comm[13:16])
        printt()
        pc+=1
    elif opc in opcode["B"].values():
        flags =["0"]*16
        typeB( opc , comm[5:8] , comm[8:16])
        printt()
        pc+=1
    elif opc in opcode["C"].values():
        typeC( opc , comm[10:13] , comm[13:16])
        printt()
        pc+=1
    elif opc in opcode["D"].values():
        flags =["0"]*16
        # plt.plot(cycle,binaryToDecimal(comm[8:16]),'bo')
        typeD( opc , comm[5:8] , comm[8:16])
        printt()
        pc+=1
    elif opc in opcode["E"].values():
        if typeE( opc , comm[8:16])!=-1:
            pass
            
        else:
            flags =["0"]*16
            printt()
            pc+=1
    cycle += 1
flags =["0"]*16
printt()

# plt.plot(cycle,pc,'bo')

for i in memory:
    print(i)

# plt.show()
