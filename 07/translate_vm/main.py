import os

from .code_writer import CodeWriter
from .parser import Parser


OUTPUT_FILE_EXT = '.asm'

STACK_IDX = 256
HEAP_IDX = 2048

def _get_output_filename(input_file):
    return os.path.splitext(input_file)[0] + OUTPUT_FILE_EXT


class Translator(object):
    def __init__(self, input_path):
        self.input_path = input_path

        output_filename = _get_output_filename(input_path)
        self.code_writer = CodeWriter(output_filename)


    def _parse_vm_file(self, vm_filename):
        parser = Parser(vm_filename)
        code_writer = self.code_writer

        code_writer.set_file_name(vm_filename)

        while parser.has_more_commands():
            parser.advance()

            command_type = parser.command_type()

            if command_type == 'C_ARITHMETIC':
                code_writer.write_arithmetic(parser.arg1())

            elif command_type == 'C_PUSH':
                code_writer.write_push_pop('C_PUSH', parser.arg1(), parser.arg2())

            elif command_type == 'C_POP':
                code_writer.write_push_pop('C_POP', parser.arg1(), parser.arg2())





    def translate(self):
        vm_path = self.input_path

        if os.path.isdir(vm_path):
            # TODO: Implement logic for multiple files in directory
            pass

        else:
            self._parse_vm_file(vm_path)



def main(vm_path):
    translator = Translator(vm_path)

    translator.translate()


if __name__ == '__main__':
    pass
