import os
import re

from .code import Code
from .parser import Parser
from .symbol_table import SymbolTable


def _get_output_dest(input_file):
    new_path = os.path.splitext(input_file)[0] + '.hack'

    return new_path


class Assembler(object):
    def __init__(self, input_file):
        self.input_file = input_file

        self.parser = Parser(input_file)
        self.encoder = Code()
        self.symbol_table = SymbolTable()


    def _first_pass(self):
        parser = self.parser

        ROM_address = 0
        while parser.hasMoreCommands():
            parser.advance()

            if parser.commandType() == 'L_COMMAND':
                symbol = parser.symbol()

                self.symbol_table.addEntry(symbol, ROM_address)

            else:
                ROM_address += 1


    def assemble(self):
        self._first_pass()

        self.parser.reset()

        output = ''

        parser = self.parser
        encoder = self.encoder

        while parser.hasMoreCommands():
            parser.advance()

            if parser.commandType() == 'L_COMMAND':
                continue

            elif parser.commandType() == 'A_COMMAND':
                line = parser.symbol()

                line = line[1:]

                if re.match('\D+.*', line):
                    if self.symbol_table.contains(line):
                        line = self.symbol_table.getAddress(line)
                    else:
                        address = self.symbol_table.get_next_available_ram_address()
                        self.symbol_table.addEntry(line, address)
                        line = address
                else:
                    line = int(line)

                line = bin(line)[2:]
                line = line.zfill(16)

            elif parser.commandType() == 'C_COMMAND':
                line = '111'
                line += encoder.comp(parser.comp())
                line += encoder.dest(parser.dest())
                line += encoder.jump(parser.jump())

            output += line + '\n'

        return output



def assemble(input_file):
    assembler = Assembler(input_file)

    output = assembler.assemble()

    with open(_get_output_dest(input_file), 'w') as f:
        f.write(output)


