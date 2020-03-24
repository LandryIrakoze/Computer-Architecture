"""CPU functionality."""

import sys


HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
ADD  = 0b10100000
MUL  = 0b10100010
CALL = 0b01010000
RET  = 0b00010001
# PUSH = 0b01000101
# POP  = 0b01000110
# JMP  = 0b01010100
# CMP  = 0b10100111
# JEQ  = 0b01010101

class CPU:
    """Main CPU class."""

    

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256


    def load(self):
        """Load a program into memory."""

        if len(sys.argv) > 1:
            loaded_program = sys.argv[1]
        
        with open(f'./examples/{loaded_program}') as file:
            data = file.read()
            print(data)

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        
        self.load()

        # for item in self.ram:
        #     print(f'item: {item}')
        
        while running:
            # command = self.ram[self.pc]
            # print(self.ram[self.pc])
            command = self.ram_read(self.pc)

            if command == HLT:
                running = False
                self.pc += 1
            elif command == LDI:
                # print(f'ram_read+1 {self.ram_read(self.pc+1)}')
                # print(f'ram_read+2 {self.ram_read(self.pc+1)}')
                self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
                self.pc += 3
                # print(f'test: {self.reg[self.pc+1]}')
                # print(f'test: {self.ram[self.pc+2]}')
                # print(f'pc+1: {self.pc+1}')
            elif command == PRN:
                # reg = self.reg
                print(self.reg[self.ram_read(self.pc+1)])
                self.pc += 2
            else:
                print(f'unknown instruction: {command}')
                sys.exit(1)

test_cpu = CPU()
test_cpu.run()
# print(f'pc: {test_cpu.pc}')


# print(f'HLT: {HLT}')
# print(f'LDI: {LDI}')
# print(f'PRN: {PRN}')