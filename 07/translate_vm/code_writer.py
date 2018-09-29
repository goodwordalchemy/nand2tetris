import os

from .asm_code.arithmetic_commands import (
    ADD_COMMAND, AND_COMMAND, EQUALS_COMMAND, GT_COMMAND,
    LT_COMMAND, NEGATE_COMMAND, NOT_COMMAND, OR_COMMAND,
    SUBTRACT_COMMAND
)
from .asm_code.push_commands import (
    PUSH_CONSTANT_COMMAND, PUSH_ARGUMENT_COMMMAND, PUSH_LOCAL_COMMAND, PUSH_POINTER_COMMAND,
    PUSH_STATIC_COMMAND, PUSH_TEMP_COMMAND, PUSH_THAT_COMMMAND, PUSH_THIS_COMMAND
)
from .asm_code.pop_commands import (
    POP_ARGUMENT_COMMAND, POP_LOCAL_COMMAND, POP_POINTER_COMMAND, POP_STATIC_COMMAND,
    POP_TEMP_COMMAND, POP_THAT_COMMAND, POP_THIS_COMMAND
)




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
        file_name = os.path.basename(file_name)
        file_name = os.path.splitext(file_name)[0]

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

            elif segment == 'local':
                asm_code = PUSH_LOCAL_COMMAND.format(index=index)

            elif segment == 'argument':
                asm_code = PUSH_ARGUMENT_COMMMAND.format(index=index)

            elif segment == 'this':
                asm_code = PUSH_THIS_COMMAND.format(index=index)

            elif segment == 'that':
                asm_code = PUSH_THAT_COMMMAND.format(index=index)

            elif segment == 'temp':
                index = str(5 + int(index))
                asm_code = PUSH_TEMP_COMMAND.format(index=index)

            elif segment == 'pointer':
                asm_code = PUSH_POINTER_COMMAND.format(index=index)

            elif segment == 'static':
                asm_code = PUSH_STATIC_COMMAND.format(
                    index=index, filename=self.current_vm_filename
                )

        elif command == 'C_POP':
            if segment == 'local':
                asm_code = POP_LOCAL_COMMAND.format(index=index)

            elif segment == 'argument':
                asm_code = POP_ARGUMENT_COMMAND.format(index=index)

            elif segment == 'this':
                asm_code = POP_THIS_COMMAND.format(index=index)

            elif segment == 'that':
                asm_code = POP_THAT_COMMAND.format(index=index)

            elif segment == 'temp':
                index = str(5 + int(index))
                asm_code = POP_TEMP_COMMAND.format(index=index)

            elif segment == 'pointer':
                asm_code = POP_POINTER_COMMAND.format(index=index)

            elif segment == 'static':
                asm_code = POP_STATIC_COMMAND.format(
                    index=index, filename=self.current_vm_filename
                )

        self.output_handle.write(asm_code)

    def close(self):
        self.output_handle.close()
