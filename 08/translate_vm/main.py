import os

from .code_writer import CodeWriter
from .parser import Parser


OUTPUT_FILE_EXT = '.asm'

STACK_IDX = 256
HEAP_IDX = 2048

def _get_output_filename(input_file):
    if os.path.isdir(input_file):
        filename = input_file.split('/')[-2]
        output_file = os.path.join(input_file, filename) + OUTPUT_FILE_EXT
    else:
        output_file =  os.path.splitext(input_file)[0] + OUTPUT_FILE_EXT

    return output_file


class Translator(object):
    def __init__(self, input_path):
        self.input_path = input_path

        output_filename = _get_output_filename(input_path)
        self.code_writer = CodeWriter(output_filename)


    def _translate_vm_file(self, vm_filename):
        parser = Parser(vm_filename)
        code_writer = self.code_writer

        code_writer.set_file_name(vm_filename)

        while parser.has_more_commands():
            parser.advance()

            command_type = parser.command_type()

            if command_type == 'C_ARITHMETIC':
                code_writer.write_arithmetic(parser.arg1())

            elif command_type in ['C_PUSH', 'C_POP']:
                code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())

            elif command_type == 'C_LABEL':
                code_writer.write_label(parser.arg1())

            elif command_type == 'C_GOTO':
                code_writer.write_goto(parser.arg1())

            elif command_type == 'C_IF':
                code_writer.write_if(parser.arg1())

            elif command_type ==  'C_FUNCTION':
                code_writer.write_function(parser.arg1(), parser.arg2())

            elif command_type == 'C_RETURN':
                code_writer.write_return()

            elif command_type == 'C_CALL':
                code_writer.write_call(parser.arg1(), parser.arg2())

            else:
                print('unknown command_type: {}'.format(command_type))

    def _translate_all_vm_files(self, vm_path):
        vm_files = [f for f in os.listdir(vm_path) if f.endswith('.vm')]

        for vm_file in vm_files:
            vm_file = os.path.join(vm_path, vm_file)

            self._translate_vm_file(vm_file)

    def translate(self):
        code_writer = self.code_writer
        code_writer.write_init()

        vm_path = self.input_path
        if os.path.isdir(vm_path):
            self._translate_all_vm_files(vm_path)

        else:
            self._translate_vm_file(vm_path)



def main(vm_path):
    translator = Translator(vm_path)

    translator.translate()


if __name__ == '__main__':
    pass
