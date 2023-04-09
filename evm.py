import sys
from collections import defaultdict

class EVM:
    def __init__(self, initial_gas):
        self.stack = []
        self.memory = bytearray()
        self.storage = defaultdict(int)
        self.pc = 0
        self.gas = initial_gas
        self.opcodes = {
            0x00: (self.op_stop, 0),
            0x01: (self.op_add, 3),
            0x02: (self.op_mul, 5),
            0x03: (self.op_sub, 3),
            0x04: (self.op_div, 5),
            0x60: (self.op_push1, 3),
        }

    def consume_gas(self, amount):
        if self.gas < amount:
            raise Exception("Out of gas")
        self.gas -= amount

    def op_stop(self, bytecode):
        return True

    def op_add(self, bytecode):
        self.stack.append((self.stack.pop() + self.stack.pop()) % 2**256)
        return False

    def op_mul(self, bytecode):
        self.stack.append((self.stack.pop() * self.stack.pop()) % 2**256)
        return False
    
    def op_sub(self, bytecode):
        self.stack.append((self.stack.pop() - self.stack.pop()) % 2**256)
        return False
    
    def op_div(self, bytecode):
        n1 = self.stack.pop()
        n2 = self.stack.pop()
        if n2 == 0:
            self.stack.append(0)
        else:
            self.stack.append((n1 // n2) % 2**256)
        return False

    def op_push1(self, bytecode):
        if self.pc >= len(bytecode):
            raise Exception("Unexpected end of bytecode")
        value = bytecode[self.pc]
        self.stack.append(value)
        self.pc += 1
        return False

    def execute(self, bytecode):
        stop_execution = False
        while self.pc < len(bytecode) and not stop_execution:
            op = bytecode[self.pc]
            self.pc += 1

            if op in self.opcodes:
                opcode_fn, gas_cost = self.opcodes[op]
                self.consume_gas(gas_cost)
                stop_execution = opcode_fn(bytecode)
            else:
                if 0x60 <= op <= 0x7f: 
                    num_bytes = op - 0x5f
                    value = int.from_bytes(bytecode[self.pc : self.pc + num_bytes], byteorder='big')
                    self.stack.append(value)
                    self.pc += num_bytes
                else:
                    raise Exception(f"Invalid opcode: {op}")


if __name__ == "__main__":
    initial_gas = 1000
    evm = EVM(initial_gas)
    bytecode = bytearray(
       [0x60, 0x05, 0x60, 0x05, 0x04, 0x00]
    )
    evm.execute(bytecode)
    print(evm.stack)
    print(f"Remaining gas: {evm.gas}")
