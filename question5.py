memoryDict = {"k" : "11" ,"K" : "10", "g" : "30", "G" : "30" , "b" : "-3" , "B" : "0" , "Word" : "" , "m" : "20","M" : "20"}
optionsMemory = "\nChoose one of the type of Addressable Memory :\n1. Bit Addressable Memory \n2. Nibble Addressable Memory\n3. Byte Addressable Memory\n4. Word Addressable Memory\n"

option =  int(input("\nChoose which question to solve :\n1. ISA and Instructions related\n2. Main memory size\n"))

if(option == 1):
    space = (input("Enter the space in memory : "))
    memoryType1 = int(input(optionsMemory))
    if memoryType1 == 1:
        memoryType1 = -3

    elif memoryType1 == 2:
        memoryType1 = -1

    elif memoryType1 == 3:
        memoryType1 = 0

    elif memoryType1 == 4:
        input1 = int(input("Enter number of bits of the CPU :"))
        for i in range(1,input1+1):
            if 2**i == (input1/8):
                memoryType1 = i
    print()
    instlen = int(input("Enter the length of one instruction in bits : "))
    reglen = int(input("Enter the length of a register in bits \t    : "))

    num1 = ""
    for i in space :
        if i in "1234567890":
            num1 = num1 + i 
    num1 = (int)(num1)
    num2 = 0

    for i in range(1,num1+1):
        if 2**i == (num1):
            num1 = i
        
    for i in  memoryDict:
        if i in space:
            num2+=int(memoryDict[i])
    m =  num2 +  num1 - memoryType1
    opcode = instlen - reglen - m
    fillerBits = instlen - opcode - 2*(reglen)
    maxInst = 2**opcode
    maxReg = 2**reglen
    print()
    print("Minimum bits needed to represent an address :", m)
    print("Number of bits needed by opcode \t    :", opcode)
    print("Number of filler bits in Type 2 Instruciton :",fillerBits)
    print("Maximum number of instruction supported     :",maxInst)
    print("Maximum number of registers supported \t    :",maxReg)


else:
    part = int(input("Choose part :\n1. Type 1\n2. Type 2\n"))
    if(part ==1):
        space = (input("Enter the space in memory : "))
        memoryType1 = int(input(optionsMemory))
        cpuBits = int(input("Enter number of bits the cpu is : "))
        if memoryType1 == 1:
            memoryType1 = -3
        elif memoryType1 == 2:
            memoryType1 = -1
        elif memoryType1 == 3:
            memoryType1 = 0
        elif memoryType1 == 4:
            for i in range(1,cpuBits+1):
                if 2**i == (cpuBits/8):
                    memoryType1 = i
        memoryType2 = int(input(optionsMemory))
        if memoryType2 == 1:
            memoryType2 = -3
        elif memoryType2 == 2:
            memoryType2 = -1
        elif memoryType2 == 3:
            memoryType2 = 0
        elif memoryType2 == 4:
            for i in range(1,cpuBits+1):
                if 2**i == (cpuBits/8):
                    memoryType2 = i
        
        print("Number of pins saved :" , memoryType1 - memoryType2)

    elif part==2:
        cpuBits = int(input("Enter number of bits of the CPU is : "))
        pins = int(input("Enter number of pins \t\t   : "))
        memoryType2 = int(input(optionsMemory))
        if memoryType2 == 1:
            memoryType2 = -3
        elif memoryType2 == 2:
            memoryType2 = -1
        elif memoryType2 == 3:
            memoryType2 = 0
        elif memoryType2 == 4:
            for i in range(1,cpuBits+1):
                if 2**i == (cpuBits/8):
                    memoryType2 = i
        
        totalmemory = pins + memoryType2
        if(totalmemory>=30):
            print("Main memory size -> " , (2**(totalmemory-30)) , "GB")
        elif(totalmemory>=20 ):
            print("Main memory size -> " , (2**(totalmemory-20)) , "mB")
        elif (totalmemory>=10):
            print("Main memory size -> " , (2**(totalmemory-10)) , "kB")
