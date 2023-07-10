
# H10L

Unimportant: The name represents Hi and Lo in the form of 1 and 0 as in digital logic.


This is the design and implementation a **custom assembler** and a **custom simulator** for a 16 bit **ISA**.\
The ISA follows **von-neumann architecture** with a unified code and data memory.
The variables are allocated in the binary in the program order.\
The automated testing infrastructure assumes that you have a working **Linux-based shell**.
For Windows, you can either use a VM or WSL.

## ISA 

### Instructions
A 16 bit ISA with the following instructions and opcodes has been considered.
The ISA has 6 encoding types of instructions.
- Type A: 3 register type
- Type B: register and immediate type
- Type C: 2 registers type
- Type D: register and memory address type
- Type E: memory address type
- Type F: halt

|Type | Opcode | Unused | REG1 | REG2 | REG3 | Immediate | MEM_addr |
|-----|--------|--------|------|------|------|-----------|----------|
|  A  |  5 bits|  2 bits|3 bits|3 bits|3 bits|           |          |
|  B  |  5 bits|        |3 bits|      |      |  8 bits   |          |
|  C  |  5 bits|  5 bits|3 bits|3 bits|      |           |          |
|  D  |  5 bits|        |3 bits|      |      |           |  8 bits  |
|  E  |  5 bits|  3 bits|      |      |      |           |  8 bits  |
|  F  |  5 bits| 11 bits|      |      |      |           |          |

### Registers
| Register | Address |
|----------|---------|
| R0       | 000     |
| R1       | 001     |
| R2       | 010     |
| R3       | 011     |
| R4       | 100     |
| R5       | 101     |
| R6       | 110     |
| FLAGS    | 111     |

### ISA Description

| Opcode | Instruction | Semantics | Syntax | Type |
|--------|-------------|-----------|--------|------|
| 10000  | Addition    | Performs reg3 = reg1 + reg2. If the computation overflows, then the overflow flag is set. | add reg1 reg2 reg3 | A    |
| 10001  | Subtraction | Performs reg3 = reg1 - reg2. In case reg2 > reg1, 0 is written to reg3 and overflow flag is set. | sub reg1 reg2 reg3 | A    |
| 10010  | Move Immediate | Performs reg1 = $Imm where Imm is an 8-bit value. | mov reg1 $Imm | B    |
| 10011  | Move Register | Performs reg2 = reg1. | mov reg1 reg2 | C    |
| 10100  | Load | Loads data from mem_addr into reg1. | ld reg1 mem_addr | D    |
| 10101  | Store | Stores data from reg1 to mem_addr. | st reg1 mem_addr | D    |
| 10110  | Multiply | Performs reg3 = reg1 x reg2. If the computation overflows, then the overflow flag is set. | mul reg1 reg2 reg3 | A    |
| 10111  | Divide | Performs reg3/reg4. Stores the quotient in R0 and the remainder in R1. | div reg3 reg4 | C    |
| 11000  | Right Shift | Right shifts reg1 by $Imm, where $Imm is an 8-bit value. | rs reg1 $Imm |    |
| 11001  | Left Shift | Left shifts reg1 by $Imm, where $Imm is an 8-bit value. | ls reg1 $Imm | B    |
| 11010  | Exclusive OR | Performs bitwise XOR of reg1 and reg2. Stores the result in reg3. | xor reg1 reg2 reg3 | A    |
| 11011  | Or | Performs bitwise OR of reg1 and reg2. Stores the result in reg3. | or reg1 reg2 reg3 | A    |
| 11100  | And | Performs bitwise AND of reg1 and reg2. Stores the result in reg3. | and reg1 reg2 reg3 | A    |
| 11101  | Invert | Performs bitwise NOT of reg1. Stores the result in reg2. | not reg1 reg2 | C    |
| 11110  | Compare | Compares reg1 and reg2 and sets up the FLAGS register. | cmp reg1 reg2 | C    |
| 11111  | Unconditional Jump | Jumps to mem_addr, where mem_addr is a memory address. | jmp mem_addr | E    |
| 01100  | Jump If Less Than | Jump to mem_addr if the less than flag is set (less than flag = 1), where mem_addr is a memory address. | jlt mem_addr | E    |
| 01101  | Jump If Greater Than | Jump to mem_addr if the greater than flag is set (greater than flag = 1), where mem_addr is a memory address. | jgt mem_addr | E    |
| 01111  | Jump If Equal | Jump to mem_addr if the equal flag is set (equal flag = 1), where mem_addr is a memory address. | je mem_addr | E    |
| 01010  | Halt | Stops the machine from executing until reset. | hlt | F    |


### FLAGS semantics
The semantics of the flags register are:
- Overflow (V): This flag is set by add, sub and mul, when the result of the operation overflows. This shows the overflow status for the last executed instruction.
- Less than (L): This flag is set by the “cmp reg1 reg2” instruction if reg1 < reg2
- Greater than (G): This flag is set by the “cmp reg1 reg2” instruction if the value of reg1 > reg2
- Equal (E): This flag is set by the “cmp reg1 reg2” instruction if reg1 = reg2 
The
default state of the FLAGS register is all zeros. If an instruction does not affect the FLAGS
register, then the state of the FLAGS register is reset to 0 upon the execution.


## Deployment

To deploy this project 
- All the run files need to be granted permission/privelidge for execution. Eg. for Linux-systems, go to the folder of each run file using bash/terminal and write 
```bash
  chmod +x run
```

- To run the results for assembler, go to Automated Testing folder and open bash/terminal. Assuming you have granted required permisions to the run file, type 
```bash
  ./run --no-sim
```

- To run the results for simulator, go to Automated Testing folder and open bash/terminal. Assuming you have granted required permisions to the run file, type
```bash
  ./run --no-asm
```

- To run the results for both,, the assembler and the simulator, go to Automated Testing folder and open bash/terminal. Assuming you have granted required permisions to the run file, type 
```bash
  ./run
```
or 

```bash
  ./run --verbose
```
