import sys
import matplotlib.pyplot as plt

x_axis=[]
y_axis=[]

types={"00000":"A","00001":"A","10000":"A","10001":"A","10110":"A","11010":"A","11011":"A","11100":"A",
"10010":"B","11001":"B","11000":"B","00010":"B",
"10011":"C","10111":"C","11101":"C","11110":"C",
"10100":"D","10101":"D",
"11111":"E","01100":"E","01101":"E","01111":"E",
"01010":"F"}                                                 #mapping opcodes to their type of instructions

registers={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}

#floating functions
def fiver(s):
    if len(s) <= 5:
        return s + (5 - len(s)) * "0"
    if len(s) > 5:
        return s[:5]

def fraction(n):
    counter = 1
    final_answer = ""
    while n != 0:
        if counter == 8:
            if n != 0:
                return "null"
            break
        else:
            n = n * 2
            final_answer += str(int(n))
            if int(n) == 1:
                n -= 1
        counter += 1
    return final_answer

def binary(n):
    g = str(format(int(n), "b"))
    return "0" * (3 - len(g)) + g

def binary_octalf(n):
    string_of_n = str(n)
    dos = list(map(int, string_of_n.split(".")))
    binary_whole_part = str(format(int(dos[0]), "b"))
    binary_fraction_part = str(fraction(n - int(n)))
    if binary_fraction_part == "null":
        message = 0
    else:
        message = binary(len(binary_whole_part[1:])) + fiver(binary_whole_part[1:] + binary_fraction_part)
    return message


def decimal(n, l):
    sum = 0
    for i in n:
        if i == ".":
            l += 1
        elif i != ".":
            sum += (2**l)*int(i)
        l -= 1
    return sum

def converter(n):
    x = int(n[:3], 2)
    if x <= 5:
        s = "1" + n[3:3+x] + "." + n[3+x:]
        return decimal(s, len("1" + n[3:3+x])-1)
    elif x == 6:
        s = "1" + n[3:8] + "0"
        return decimal(s, len(s)-1)
    elif x == 7:
        s = "1" + n[3:8] + "00"
        return decimal(s, len(s)-1)

REG=[]                          #will store int register values having R"1" as index
for i in range(8):
    REG.append("0000000000000000")
                               
MEM=[]                           #a list of 256 values initialized as 0s having int("binary number") as index
for i in range(256):
    MEM.append("0000000000000000")

def reset_flags():           #resets all flags
    REG[7]="0000000000000000"

def get_val(r):                   #returns int value from reg
    val=REG[int(r[1])]
    return int(val,2)

def get_valf(r):
    val=REG[int(r[1])]
    val = converter(val)
    return val

def store_val(r,val):             #stores int value as 16 bit bin in reg
    g=str(format(val,"b"))
    g="0"*(16-len(g))+g
    REG[int(r[1])]=g
    return

def check_overflow(s):
    if s>(2**16):
        s=s%(2**16)
        REG[7]="0000000000001000"
    return s

def bitwise_not(a,r):
    a=list(a)
    for i in range(len(a)):
        if a[i]=="0":
            a[i]='1'
        else:
            a[i]='0'
    a="".join(a)
    REG[int(r[1])]=a
    return


def execute_type_a(op,inst):         #r3=r2+r1
    r3=registers[inst[13:16]]
    r2=registers[inst[10:13]]
    r1=registers[inst[7:10]]

    if op=="10000": #add
        s=get_val(r2)+get_val(r1)
        s=check_overflow(s)
        store_val(r3,s)

    elif op=="10001": #sub
        s=get_val(r1)-get_val(r2)
        if s<0:
            s=0
            REG[7]="0000000000001000"
        store_val(r3,s)

    elif op=="11010": #xor
        s=get_val(r1)^get_val(r2)
        store_val(r3,s)

    elif op=="11011": #or
        s=get_val(r1) | get_val(r2)
        store_val(r3,s)

    elif op=="11100": #and
        s=get_val(r1) & get_val(r2)
        store_val(r3,s)

    elif op=="10110": #mul
        s=get_val(r1)*get_val(r2)
        s=check_overflow(s)
        store_val(r3,s)

    elif op=="00000": #addf                    #first convert from r(8 bit) to float then add float then float to 8 bit;
        s=get_valf(r1)+get_valf(r2)
        s=binary_octalf(s)
        if s==0:
            REG[int(r3[1])]="0000000000000000"
            REG[7]="0000000000001000"
        else:
            s="0"*(16-len(s))+s
            REG[int(r3[1])]=s
        

    elif op=="00001": #subf
        s=get_valf(r1)-get_valf(r2)
        s=binary_octalf(s)
        if s==0:
            REG[int(r3[1])]="0000000000000000"
            REG[7]="0000000000001000"
        else:
            s="0"*(16-len(s))+s
            REG[int(r3[1])]=s
    

def execute_type_b(op,inst):
    imm=int(inst[8:],2)
    r=registers[inst[5:8]]
    if op=="10010": #store
        store_val(r,imm)

    elif op=="00010": #movf
        imm=str(imm)
        s="0"*(16-len(imm))+imm
        REG[int(r[1])]=s

    elif op=="11000": #rs
        s=get_val(r)
        s=s>>imm
        if s<0:
            s=0
            REG[7]="0000000000001000"
        store_val(r,s)
    elif op=="11001": #ls
        s=get_val(r)
        s=s<<imm
        s=check_overflow(s)
        store_val(r,s)
    

def execute_type_c(op,inst):
    r2=registers[inst[13:16]]
    r1=registers[inst[10:13]]
    if op=="10011": #mov
        if r1=="FLAGS":
            REG[int(r2[1])]=REG[7]
        else:
            store_val(r2,get_val(r1))

    elif op=="10111": #div
        q=get_val(r1)//get_val(r2)
        r=get_val(r1)%get_val(r2)
        store_val("R0",q)
        store_val("R1",r)

    elif op=="11101": #invert
        n=REG[int(r1[1])]
        n=bitwise_not(n,r2)

    elif op=="11110": #cmp
        a=get_val(r1)
        b=get_val(r2)
        if a>b:
            REG[7]="0000000000000010"
        elif a==b:
            REG[7]="0000000000000001"
        else:
            REG[7]="0000000000000100"


def execute_type_d(op,inst,pc):
    mem_adr=inst[8:]
    mem_adr=int(mem_adr,2)
    r=registers[inst[5:8]]
    if op=="10100": #ld
        data=int(MEM[mem_adr],2)
        store_val(r,data)
    elif op=="10101": #st
        s=get_val(r)
        g=str(format(s,"b"))
        g="0"*(16-len(g))+g 
        MEM[mem_adr]=g
    x_axis.append(cycles)
    y_axis.append(mem_adr)
    


def execute_type_e(op,inst,pc):
    mem_adr=inst[8:]
    mem_adr=int(mem_adr,2)

    if op=="11111": #jmp
        pc=mem_adr
    elif op=="01100": #jlt 
        if(REG[7][13]=="1"):
            pc=mem_adr
    elif op=="01101": #jgt
        if(REG[7][14]=="1"):
            pc=mem_adr
    elif op=="01111": #je
        if(REG[7][15]=="1"):
            pc=mem_adr
    return pc

def print_values(pc):
    pc=str(format(pc,"b"))
    pc="0"*(8-len(pc))+pc
    print(pc,end=" ")

    for i in range(7):
        print(REG[i],end=" ")
    print(REG[7])

def end(pc):
    print_values(pc)
    for i in MEM:
        print(i)

#start of program

data =[i for i in sys.stdin.readlines()]

for i in range(len(data)):
    if len(data[i])>16:
        MEM[i]=data[i][:16]
    if i==255:
        break

cycles=0
pc = 0
flag=0
while pc<len(MEM):
    inst=MEM[pc]
    opcode=inst[:5]
    t=types[opcode]

    x_axis.append(cycles)
    y_axis.append(pc)
    if t=="A":
        execute_type_a(opcode,inst)
    elif t=="B":
        execute_type_b(opcode,inst)
    elif t=="C":
        execute_type_c(opcode,inst)
    elif t=="D":
        execute_type_d(opcode,inst,pc)
    elif t=="E":
        new_pc=execute_type_e(opcode,inst,pc)
        if new_pc!=pc:
            flag=1
    elif t=="F":
        end(pc)
        break

    if opcode=='11110':
        if MEM[pc+1][:3]=='011' or MEM[pc+1][:13]=='1001100000111':
            pass
        else:
            reset_flags()
    else:
        reset_flags()

    print_values(pc)
    if flag!=0:
        pc=new_pc
        flag=0
    else:
        pc+=1
    cycles+=1

plt.ylabel("Memory Address (line number)")
plt.xlabel("Cycles")
plt.title('Memory Addresses accessed per cycle')
plt.scatter(x_axis,y_axis)
plt.show()