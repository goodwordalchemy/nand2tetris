import re

ARITHMETIC_COMMANDS = [
    'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'
]
PERMISSABLE_ARG2_COMMAND_TYPES = ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']

def _clean_input(lines):
    clean_input = []

    for command in lines:
        comment_match = re.search(r'//', command)
        if comment_match:
            command = command[:comment_match.start()]

        command = ' '.join(command.split())

        if command:
            clean_input.append(command)

    return clean_input


class Parser(object):

    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            input_lines = f.readlines()

        input_lines = _clean_input(input_lines)

        self.input_lines = input_lines
        self.input_file_length = len(self.input_lines)

        self.current_line = -1
        self.current_command = None

    def has_more_commands(self):
        return self.current_line < self.input_file_length - 1

    def advance(self):
        self.current_line += 1
        self.current_command = self.input_lines[self.current_line]

    def command(self):
        return self.current_command.split()[0]

    def command_type(self):
        command = self.command()

        if command in ARITHMETIC_COMMANDS:
            return 'C_ARITHMETIC'

        if command == 'push':
            return 'C_PUSH'

        if command == 'pop':
            return 'C_POP'

        if command == 'label':
            return 'C_LABEL'

        if command == 'goto':
            return 'C_GOTO'

        if command == 'if-goto':
            return 'C_IF'

        if command == 'function':
            return 'C_FUNCTION'

        if command == 'return':
            return 'C_RETURN'

        if command == 'call':
            return 'C_CALL'

    def arg1(self):
        if self.command_type() == 'C_RETURN':
            raise Exception('arg1 should not be called if current command type is "C_RETURN"')

        line_split = self.current_command.split()

        if self.command_type() == 'C_ARITHMETIC':
            return line_split[0]

        if len(line_split) > 1:
            return line_split[1]

    def arg2(self):
        if self.command_type() not in PERMISSABLE_ARG2_COMMAND_TYPES:
            exception_string_format = (
                'arg2 was called with command type: "{}".'
                'It should only be called with command types: {}'
            )
            raise Exception(exception_string_format.format(self.command_type(), PERMISSABLE_ARG2_COMMAND_TYPES))

        line_split = self.current_command.split()

        if len(line_split) > 2:
            return line_split[2]
