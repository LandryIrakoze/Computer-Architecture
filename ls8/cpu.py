"""CPU functionality."""

import sys

from instructions import *


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.sp = 7
        self.reg = [0] * 8
        self.ram = [0] * 256

        self.branchtable = {}

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: file.py filename")
            sys.exit(1)

        loaded_program = sys.argv[1]

        try:
            address = 0
            
            with open(f'./examples/{loaded_program}') as file:
                for line in file:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        alu_branchtable = {}

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "ADI":
            pass
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
            self.pc += 3
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
            self.pc += 3
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
            self.pc += 3
        elif op == "NOT":
            self.reg[reg_a] = ~ self.reg[reg_a] 
            self.pc += 2
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
            self.pc += 3
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
            self.pc += 3
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
            self.pc += 3
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == "CMP":
            if reg_a < reg_b:
                FL = LT
                self.pc += 3
            elif reg_a > reg_b:
                FL = GT
                self.pc += 3
            elif reg_a == reg_b:
                FL = ET
                self.pc += 3
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

        while running:
            command = self.ram_read(self.pc)
                            
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if command == HLT:
                running = False
                self.pc += 1
            elif command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif command == ADD:
                self.alu('ADD', operand_a, operand_b)
            elif command == MUL:
                self.alu('MUL', operand_a, operand_b)
            elif command == PUSH:
                val = self.reg[operand_a]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc += 2
            elif command == POP:
                val = self.ram[self.reg[self.sp]]
                self.reg[operand_a] = val
                self.reg[self.sp] += 1
                self.pc += 2
            elif command == CALL:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                self.pc = self.reg[operand_a]
            elif command == RET:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
            elif command == CMP:
                self.alu('CMP', operand_a, operand_b)
            elif command == JMP:
                self.pc = self.reg[operand_a]
                # self.pc == self.ram[self.reg[operand_a]]
            elif command == JEQ:
                if FL == ET:
                    self.pc = self.reg[operand_a]
                    # self.pc = self.ram[self.reg[operand_a]]
                else:
                    self.pc += 2
            elif command == JNE:
                if FL != ET:
                    self.pc = self.reg[operand_a]
                    # self.pc = self.ram[self.reg[operand_a]]
                else:
                    self.pc += 2
            else:
                print(f'unknown instruction: {command}')
                sys.exit(1)
