import re


def _clean_input(lines):
    clean_input = []

    for command in lines:
        comment_match = re.search(r'//', command)
        if comment_match:
            command = command[:comment_match.start()]

        command = ''.join(command.split())

        if command:
            clean_input.append(command)

    return clean_input


class Parser(object):

    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            input_file = f.readlines()

        self.input = _clean_input(input_file)

        self.current_command = None
        self.pc = -1  # Processed up to line number.

    def hasMoreCommands(self):
        return len(self.input) > self.pc

    def advance(self):
        self.pc += 1
        if self.hasMoreCommands():
            self.current_command =  self.input[self.pc]

    def commandType(self):
        if re.match('@[\w+|\d+\.\d*]', self.current_command):
            return 'A_COMMAND'
        elif re.match('\(\w+\)', self.current_command):
            return 'L_COMMAND'
        return 'C_COMMAND'

    def symbol(self):
        if self.commandType() == 'L_COMMAND':
            return re.match('\((\w+)\)', self.current_command).string

        if self.commandType() == 'A_COMMAND':
            return re.match('@(.+)', self.current_command).string

    def dest(self):
        if self.commandType() == 'C_COMMAND':
            dest = self.current_command

            if '=' in dest:
                return dest.split('=')[0]

            return ''

    def comp(self):
        if self.commandType() == 'C_COMMAND':
            comp = self.current_command

            if '=' in comp:
                comp = comp.split('=')[1]

            if ';' in comp:
                comp = comp.split(';')[0]

        return comp

    def jump(self):
        if self.commandType() == 'C_COMMAND':
            jump = self.current_command

            if ';' in jump:
                return jump.split(';')[1]

            return ''
