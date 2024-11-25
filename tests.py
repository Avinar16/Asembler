import unittest
import subprocess
import os
import xml.etree.ElementTree as ET
from assembler import assemble
from interpreter import interpret


def parse_result_file(file_path):
    memory = {}
    tree = ET.parse(file_path)
    root = tree.getroot()

    for memory_entry in root:
        address = int(memory_entry.get('address', -1))
        value = int(memory_entry.text.strip() if memory_entry.text else 0)
        memory[address] = value
    print(memory)
    return memory


class TestAssembler(unittest.TestCase):
    def test_load_const(self):
        program = 'LOAD_CONST 137\nSTORE_MEM 0'
        with open('assembly_test.asm', 'w') as f:
            f.write(str(program))

        input_program = "assembly_test.asm"
        binary_file = 'binary_op_equal.bin'
        result_file = 'result.xml'
        log_file = "log.xml"

        assemble(input_program, binary_file, log_file)
        interpret(binary_file, result_file, "0-1")

        memory = parse_result_file(result_file)
        self.assertEqual(memory[0], 137)

    def test_load_mem(self):
        program = "LOAD_CONST 252\nSTORE_MEM 6\nLOAD_MEM 6"
        with open('assembly_test.asm', 'w') as f:
            f.write(str(program))

        input_program = "assembly_test.asm"
        binary_file = 'binary_op_equal.bin'
        result_file = 'result.xml'
        log_file = "log.xml"

        assemble(input_program, binary_file, log_file)
        interpret(binary_file, result_file, "6-7")

        # Проверяем, что значение из памяти корректно загружено
        memory = parse_result_file(result_file)
        self.assertEqual(memory[6], 252)

    def test_store_mem(self):
        # Программа для записи значения в память
        program = "LOAD_CONST 206\nSTORE_MEM 7"
        with open('assembly_test.asm', 'w') as f:
            f.write(str(program))

        input_program = "assembly_test.asm"
        binary_file = 'binary_op_equal.bin'
        result_file = 'result.xml'
        log_file = "log.xml"

        assemble(input_program, binary_file, log_file)
        interpret(binary_file, result_file, "7-8")

        memory = parse_result_file(result_file)
        self.assertEqual(memory[7], 206)

    def test_binary_op_equal(self):
        # Программа для сравнения двух чисел
        program = """
        LOAD_CONST 974\n
        STORE_MEM 1\n
        LOAD_MEM 1\n
        LOAD_CONST 974\n
        BINARY_OP ==\n
        STORE_MEM 2
        """
        with open('assembly_test.asm', 'w') as f:
            f.write(str(program))

        input_program = "assembly_test.asm"
        binary_file = 'binary_op_equal.bin'
        result_file = 'result.xml'
        log_file = "log.xml"

        assemble(input_program, binary_file, log_file)
        interpret(binary_file, result_file, "1-3")

        memory = parse_result_file(result_file)
        self.assertEqual(memory[2], 1)


if __name__ == '__main__':
    unittest.main()
