import sys
reg={"R0" : "000" ,"R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110"}

opcode = {
"A" : {"add" : "10000" , "sub" : "10001" , "mul" : "10110" , "xor" : "11010" , "and" : "11100", "or":"11011"}, 
"B" : {"mov" : "10010" , "ls" : "11001","rs":"11000"}, 
"C" : {"mov" : "10011"  ,"div" : "10111" , "not" : "11101" , "cmp" : "11110"},
"D" : {"ld" : "10100" , "st" : "10101"},
"E" : {"jmp" : "11111" , "jlt" : "01100" , "jgt" : "01101" , "je" : "01111"},
"F" : {"hlt" : "01010"} 
}                  

error = 0 
variable = {}
label = {}
machineCodes = []
programCounter = 0




inst0=[i.split() for i in sys.stdin.readlines()]

instructions=inst0.copy()
inst=[]
for i in instructions:
    if i:
        inst.append(i)


if len(inst)>256:                 
    print("Memory Overflow")
    error=1

for i in variable:
    if(not check(i)):
        print("Line",i+1,"Invalid variable definition")
        error=1
    
for i in label:
    if(not check(i)):
        print("Line",i+1,"Invalid label definition")
        error=1

inst = variables(inst)
if error == 0 :
    inst = labels(inst)


for i in variable:
    if(not check(i)):
        print("Line",int(variable[i])-len(inst)+1,"Invalid variable definition")
        error=1
    
for i in label:
    if(not check(i)) and error==0:
        print("Line",int(label[i])+1+len(variable),"Invalid label definition")
        error=1
      
if(error == 0):
    for i in range(len(inst)-1):
        if inst[i]==['hlt']:
            error=1
            print("Line",i+len(variable)+1,"hlt called before other instructions")
    if inst[-1]!=['hlt']:
        error=1
        print("Line",len(inst)+len(variable),"Last instruction not hlt")
if(error == 0):
    for i in range(len(inst)):
        ispresent=False 
        for key in opcode:
            if inst[i][0] in opcode[key]:
                ispresent=True
                break
        if not ispresent:
            print("Line",i+1+len(variable),"Wrong Instruction Name")
            error = 1
            break
        if error == 0 :
            if inst[i][0]=='mov':
                if inst[i][2][0]=='$':
                    typeB(inst[i],i)
                else:
                    typeC(inst[i],i)
            else :
                for key in opcode:
                    if inst[i][0] in opcode[key]:
                        if key=='A':
                            typeA(inst[i],i)
                        elif key=='B':
                            typeB(inst[i],i)
                        elif key=='C':
                            typeC(inst[i],i)
                        elif key=='D':
                            typeD(inst[i],i)
                        elif key=='E':
                            typeE(inst[i],i)
                        elif key=='F':
                            typeF(inst[i],i)
        else:
            break
    if error == 0 :
        for codes in machineCodes:
            print(codes)  
