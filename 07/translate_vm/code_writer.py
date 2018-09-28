from .asm_code.arithmetic_commands import (
    ADD_COMMAND, AND_COMMAND, EQUALS_COMMAND, GT_COMMAND,
    LT_COMMAND, NEGATE_COMMAND, NOT_COMMAND, OR_COMMAND,
    SUBTRACT_COMMAND
)

PUSH_CONSTANT_COMMAND = '''
// // push constant x
@{index}
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
'''

class SequentialNumberGenerator(object):
    def __init__(self, start=0):
        self.current = -1

    def generate(self):
        self.current += 1

        return self.current


class CodeWriter(object):
    def __init__(self, output_file):
        self.output_handle = open(output_file, 'w')
        self.label_index_generator = SequentialNumberGenerator()

    def set_file_name(self, file_name):
        self.current_vm_filename = file_name

    def write_arithmetic(self, command):
        if command == 'add':
            asm_code = ADD_COMMAND

        elif command == 'sub':
            asm_code = SUBTRACT_COMMAND

        elif command == 'neg':
            asm_code = NEGATE_COMMAND

        elif command == 'eq':
            asm_code = EQUALS_COMMAND.format(
                unique_label=self.label_index_generator.generate()
            )

        elif command == 'gt':
            asm_code = GT_COMMAND.format(
                unique_label=self.label_index_generator.generate()
            )

        elif command == 'lt':
            asm_code = LT_COMMAND.format(
                unique_label=self.label_index_generator.generate()
            )

        elif command == 'and':
            asm_code = AND_COMMAND

        elif command == 'or':
            asm_code = OR_COMMAND

        elif command == 'not':
            asm_code = NOT_COMMAND

        self.output_handle.write(asm_code)

    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            if segment == 'constant':
                asm_code = PUSH_CONSTANT_COMMAND.format(index=index)

        self.output_handle.write(asm_code)

    def close(self):
        self.output_handle.close()
