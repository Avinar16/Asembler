class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size
        self.stack = []

    def load_constant(self, value):
        self.stack.append(value)

    def load_from_memory(self, address):
        self.stack.append(self.memory[address])

    def store_to_memory(self, address):
        value = self.stack.pop()
        self.memory[address] = value

    def binary_operation(self, operation):
        b = self.stack.pop()
        a = self.stack.pop()
        if operation == "==":
            self.stack.append(1 if a == b else 0)

    def execute(self, program):
        for instruction in program:
            opcode = instruction["opcode"]

            if opcode == "LOAD_CONST":
                self.load_constant(instruction["value"])
            elif opcode == "LOAD_MEM":
                self.load_from_memory(instruction["address"])
            elif opcode == "STORE_MEM":
                self.store_to_memory(instruction["address"])
            elif opcode == "BINARY_OP":
                self.binary_operation(instruction["operation"])
