import unittest
from evm import EVM 

class TestEVM(unittest.TestCase):
    def test_push1(self):
        print('PUSH1')
        evm = EVM(1000)
        bytecode = bytearray([0x60, 0x0A])  # PUSH1 0x0A
        evm.execute(bytecode)
        self.assertEqual(evm.stack, [0x0A])

    def test_add(self):
        print('ADD')
        evm = EVM(1000)
        bytecode = bytearray([0x60, 0x03, 0x60, 0x02, 0x01])  # PUSH1 0x03, PUSH1 0x02, ADD
        evm.execute(bytecode)
        self.assertEqual(evm.stack, [0x05])

    def test_sub(self):
        print('SUB')
        evm = EVM(1000)
        bytecode = bytearray([0x60, 0x03, 0x60, 0x02, 0x03])  # PUSH1 0x03, PUSH1 0x02, SUB
        evm.execute(bytecode)
        self.assertEqual(evm.stack, [0x01])

    def test_mul(self):
        print('MUL')
        evm = EVM(1000)
        bytecode = bytearray([0x60, 0x03, 0x60, 0x02, 0x02])  # PUSH1 0x03, PUSH1 0x02, MUL
        evm.execute(bytecode)
        self.assertEqual(evm.stack, [0x06])

    def test_div(self):
        print('DIV')
        evm = EVM(1000)
        bytecode = bytearray([0x60, 0x06, 0x60, 0x03, 0x04])  # PUSH1 0x06, PUSH1 0x03, DIV
        evm.execute(bytecode)
        self.assertEqual(evm.stack, [0x02])

    def test_out_of_gas(self):
        print('OUT OF GAS')
        evm = EVM(2)
        bytecode = bytearray([0x60, 0x03, 0x60, 0x02, 0x01])  # PUSH1 0x03, PUSH1 0x02, ADD
        with self.assertRaises(Exception) as context:
            evm.execute(bytecode)
        self.assertEqual(str(context.exception), "Out of gas")

    def test_invalid_opcode(self):
        print('INVALID OPCODE')
        evm = EVM(1000)
        bytecode = bytearray([0xFF])  # Invalid opcode
        with self.assertRaises(Exception) as context:
            evm.execute(bytecode)
        self.assertEqual(str(context.exception), "Invalid opcode: 255")

if __name__ == "__main__":
    unittest.main()
