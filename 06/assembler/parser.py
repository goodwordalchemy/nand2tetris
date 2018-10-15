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

        self.reset()

    def reset(self):
        self.current_command = None
        self.line_num_in_file = -1

    def hasMoreCommands(self):
        return len(self.input) > self.line_num_in_file + 1

    def advance(self):
        if not self.hasMoreCommands():
            raise Exception('No more commands in file')

        self.line_num_in_file += 1

        self.current_command =  self.input[self.line_num_in_file]

    def commandType(self):
        if re.match('@[\D+.+|\d+\.\d*]', self.current_command):
            return 'A_COMMAND'

        elif re.match('\(\D+.*\)', self.current_command):
            return 'L_COMMAND'
        return 'C_COMMAND'

    def symbol(self):
        if self.commandType() == 'L_COMMAND':
            match = re.match('\((\D+.*)\)', self.current_command)

            if match:
                return match.group(1)

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
