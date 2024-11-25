import struct
import xml.etree.ElementTree as ET
import sys


def assemble(input_file, output_file, log_file):
    program = []
    log = []

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("LOAD_CONST"):
                _, value = line.split()
                value = int(value)
                program.append({"opcode": "LOAD_CONST", "value": value})
                log.append(f"opcode=LOAD_CONST value={value}")
            elif line.startswith("LOAD_MEM"):
                _, address = line.split()
                address = int(address)
                program.append({"opcode": "LOAD_MEM", "address": address})
                log.append(f"opcode=LOAD_MEM address={address}")
            elif line.startswith("STORE_MEM"):
                _, address = line.split()
                address = int(address)
                program.append({"opcode": "STORE_MEM", "address": address})
                log.append(f"opcode=STORE_MEM address={address}")
            elif line.startswith("BINARY_OP"):
                _, operation = line.split()
                program.append({"opcode": "BINARY_OP", "operation": operation})
                log.append(f"opcode=BINARY_OP operation={operation}")

    # Запись в бинарный файл
    with open(output_file, "wb") as f:
        for instruction in program:
            if instruction["opcode"] == "LOAD_CONST":
                f.write(struct.pack("B", 0))
                if instruction["value"] > 255:
                    f.write(struct.pack("H", instruction["value"]))
                else:
                    f.write(struct.pack("B", instruction["value"]))
            elif instruction["opcode"] == "LOAD_MEM":
                f.write(struct.pack("B", 6))  # чтения из памяти
                f.write(struct.pack("B", instruction["address"]))
            elif instruction["opcode"] == "STORE_MEM":
                f.write(struct.pack("B", 7))  # записи в память
                f.write(struct.pack("B", instruction["address"]))
            elif instruction["opcode"] == "BINARY_OP":
                f.write(struct.pack("B", 1))  # ==
                f.write(struct.pack("B", 0))
    # Лог в XML
    root = ET.Element("log")
    for entry in log:
        log_entry = ET.SubElement(root, "entry")
        log_entry.text = entry
    tree = ET.ElementTree(root)
    tree.write(log_file)


if __name__ == '__main__':
    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
