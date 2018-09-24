import os

from .parser import Parser
from .code import Code


def _get_output_dest(input_file):
    new_path = os.path.splitext(input_file)[0] + '.hack'

    return new_path

def assemble(input_file):
    output = ''
    parser = Parser(input_file)

    encoder = Code()

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == 'A_COMMAND':
            line = parser.symbol()
            line = int(line[1:])
            line = bin(line)[2:]
            line = line.zfill(16)

        elif parser.commandType() == 'C_COMMAND':
            line = '111'
            line += encoder.comp(parser.comp())
            line += encoder.dest(parser.dest())
            line += encoder.jump(parser.jump())

        output += line + '\n'


    with open(_get_output_dest(input_file), 'w') as f:
        f.write(output)


