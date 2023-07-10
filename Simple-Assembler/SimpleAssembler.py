import sys

reg = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]


def raised_error(err):
    print(err)
    exit()


def fiver(s):
    if len(s) <= 5:
        return s + (5 - len(s)) * "0"
    if len(s) > 5:
        return s[:5]


def binary(n):
    g = str(format(int(n), "b"))
    return "0" * (3 - len(g)) + g


def binary_octal(n):
    g = str(format(int(n), "b"))
    return "0" * (8 - len(g)) + g


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


def check_immf(s, lc):
    if binary_octalf(s) == 0:
        err = "Immediate Value out of range Error at line no. " + str(lc)
        raised_error(err)
    return 1


def check_register_name(l, n, lc):
    for i in range(1, n):
        if l[i].lower() == "flags":
            err = "Illegal use of FLAGS register Error at line no. " + str(lc)
            raised_error(err)
        if l[i] not in reg:
            err = "Register Name Error at line no. " + str(lc)
            raised_error(err)
    return 1


def check_label(d, s, lc):
    if s not in d:
        err = "Undefined Label Error at line no. " + str(lc)
        raised_error(err)
    if s in variables:
        err = "Misuse of Variable as Label Error at line no. " + str(lc)
        raised_error(err)
    return 1


def check_var(d, s, lc):
    if s not in d:
        err = "Undefined Variable Error at line no. " + str(lc)
        raised_error(err)
    if s in labels:
        err = "Misuse of Label as Variable Error at line no. " + str(lc)
        raised_error(err)
    return 1


def check_count(l, c, lc):
    if len(l) != c:
        err = "General Syntax Error at line no. " + str(lc)
        raised_error(err)
    return 1


def check_imm(s, lc):
    if int(s) not in range(256):
        err = "Immediate Value out of range Error at line no. " + str(lc)
        raised_error(err)
    return 1


def assemble(l, lc):
    opcode = {"add": "1000000", "sub": "1000100", "ld": "10100", "st": "10101", "mul": "1011000",
              "div": "1011100000", "rs": "11000", "ls": "11001", "xor": "1101000", "or": "1101100",
              "and": "1110000", "not": "1110100000", "cmp": "1111000000", "jmp": "11111000",
              "jlt": "01100000", "jgt": "01101000", "je": "01111000", "hlt": "0101000000000000", "mov": "0"}

    if l[0] not in opcode:
        err = "Instruction Name Error at line no. " + str(lc)
        raised_error(err)

    elif l[0] == "add":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "1000000" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "addf":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "0000000" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "sub":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "1000100" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "subf":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "0001000" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "movf":
        if check_register_name(l, 2, lc) and check_immf(l[2][1:], lc):
            return "10010" + binary(l[1][1]) + binary_octalf(l[2][1:])
        return 0

    elif l[0] == "mov":
        if check_count(l, 4, lc):
            if l[2][0] == "$":
                if check_register_name(l, 2, lc) and check_imm(l[2][1:], lc):
                    return "10010" + binary(l[1][1]) + binary_octal(l[2][1:])
                return 0
            else:
                for i in range(1, 3):
                    if l[i].lower() == "flags" and i != 1:
                        err = "Illegal use of FLAGS register Error at line no. " + str(lc)
                        raised_error(err)
                    if l[i] not in reg and l[i] != "FLAGS":
                        err = "Register Name Error at line no. " + str(lc)
                        raised_error(err)
                if l[1] == "FLAGS":
                    return "1001100000" + "111" + binary(l[2][1])
                else:
                    return "1001100000" + binary(l[1][1]) + binary(l[2][1])
        else:
            return 0

    elif l[0] == "ld":
        if check_count(l, 4, lc) and check_var(mem_adr, l[2], lc) and check_register_name(l, 2, lc):
            return "10100" + binary(l[1][1]) + mem_adr[l[2]]
        return 0

    elif l[0] == "st":
        if check_count(l, 4, lc) and check_var(mem_adr, l[2], lc) and check_register_name(l, 2, lc):
            return "10101" + binary(l[1][1]) + mem_adr[l[2]]
        return 0

    elif l[0] == "mul":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "1011000" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "div":
        if check_count(l, 4, lc) and check_register_name(l, 3, lc):
            return "1011100000" + binary(l[1][1]) + binary(l[2][1])
        return 0

    elif l[0] == "rs":
        if check_count(l, 4, lc) and check_register_name(l, 2, lc) and check_imm(l[2][1:], lc):
            return "11000" + binary(l[1][1]) + binary_octal(l[2][1:])
        return 0

    elif l[0] == "ls":
        if check_count(l, 4, lc) and check_register_name(l, 2, lc) and check_imm(l[2][1:], lc):
            return "11001" + binary(l[1][1]) + binary_octal(l[2][1:])
        return 0

    elif l[0] == "xor":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "1101000" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "or":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "1101100" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "and":
        if check_count(l, 5, lc) and check_register_name(l, 4, lc):
            return "1110000" + binary(l[1][1]) + binary(l[2][1]) + binary(l[3][1])
        return 0

    elif l[0] == "not":
        if check_count(l, 4, lc) and check_register_name(l, 3, lc):
            return "1110100000" + binary(l[1][1]) + binary(l[2][1])
        return 0

    elif l[0] == "cmp":
        if check_count(l, 4, lc) and check_register_name(l, 3, lc):
            return "1111000000" + binary(l[1][1]) + binary(l[2][1])
        return 0

    elif l[0] == "jmp":
        if check_count(l, 3, lc) and check_label(mem_adr, l[1], lc):
            return "11111000" + mem_adr[l[1]]
        return 0

    elif l[0] == "jlt":
        if check_count(l, 3, lc) and check_label(mem_adr, l[1], lc):
            return "01100000" + mem_adr[l[1]]
        return 0

    elif l[0] == "jgt":
        if check_count(l, 3, lc) and check_label(mem_adr, l[1], lc):
            return "01101000" + mem_adr[l[1]]
        return 0

    elif l[0] == "je":
        if check_count(l, 3, lc) and check_label(mem_adr, l[1], lc):
            return "01111000" + mem_adr[l[1]]
        return 0

    elif l[0] == "hlt":
        if check_count(l, 2, lc):
            return "0101000000000000"
        return 0


global mem_adr
global labels
global variables
global output
mem_adr = {}
variables = {}
labels = {}
output = []

i = 0
instructions = []
total_vars = 0
line_count = 0

data = [i for i in sys.stdin.readlines()]

if data.count("hlt\n") == 0:
    s = list(map(str, data[len(data)-2].split()))
    if ":" in s[0] and s[1] != "hlt":
        err = "Missing halt instruction at line no. " + str(len(data)-1)
        raised_error(err)

temp_data = data.copy()
temp_data.pop()

if "hlt\n" in temp_data:
    err = "Incorrect use of Halt Instruction at line no." + str(temp_data.index("hlt\n") + 1)
    raised_error(err)

for line in data:
    s = list(map(str, line.split()))
    if s == []:
        continue
    if s[0] == "var":
        total_vars += 1
    if s[0] != "var":
        s += [binary_octal(i)]
        i += 1
    if ":" in s[0] and (data.index(line) != len(data) - 2):
        mem_adr[s[0][0:len(s[0]) - 1]] = s[-1]
        labels[s[0][0:len(s[0]) - 1]] = s[-1]
    if ":" in s[0] and (data.index(line) == len(data) - 2):
        if s[1] == "hlt\n":
            mem_adr[s[0][0:len(s[0]) - 1]] = s[-1]
            labels[s[0][0:len(s[0]) - 1]] = s[-1]
    instructions += [s]

for k in range(total_vars):
    if instructions[k][0] != "var":
        err = "All variables not declared at the start Error"
        raised_error(err)

for k in instructions:
    line_count += 1
    if k[0] == "var":
        mem_adr[k[1]] = binary_octal(i)
        variables[k[1]] = binary_octal(i)
        i += 1
    else:
        if ":" in k[0]:
            k.pop(0)
        ret = assemble(k, line_count)
        output.append(ret)

for i in output:
    print(i)
