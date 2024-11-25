import xml.etree.ElementTree as ET
from vm import VirtualMachine
import sys
import struct


def interpret(binary_file, result_file, memory_range):
    start, end = map(int, memory_range.split('-'))

    vm = VirtualMachine()
    program = []

    with open(binary_file, "rb") as f:
        while byte := f.read(1):
            opcode = struct.unpack("B", byte)[0]
            if opcode == 0:
                value = struct.unpack("B", f.read(1))[0]
                program.append({"opcode": "LOAD_CONST", "value": value})
            elif opcode == 6:
                address = struct.unpack("B", f.read(1))[0]
                program.append({"opcode": "LOAD_MEM", "address": address})
            elif opcode == 7:
                address = struct.unpack("B", f.read(1))[0]
                program.append({"opcode": "STORE_MEM", "address": address})
            elif opcode == 1:
                operation = struct.unpack("B", f.read(1))[0]
                if operation == 0:
                    program.append({"opcode": "BINARY_OP", "operation": "=="})

    vm.execute(program)

    # Сохранение памяти в XML
    root = ET.Element("memory")
    for address in range(start, end + 1):
        cell = ET.SubElement(root, "cell")
        cell.set("address", str(address))
        cell.text = str(vm.memory[address])

    tree = ET.ElementTree(root)
    tree.write(result_file)


if __name__ == '__main__':
    interpret(sys.argv[1], sys.argv[2], sys.argv[3])
