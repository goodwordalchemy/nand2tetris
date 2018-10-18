TAB = '\t'

OP_SYMBOL_TO_VM_COMMAND_MAPPER = {
    '+': 'add', '-': 'sub', '*': 'Math.multiply', '/': 'Math.divide',
    '&amp;': 'and', '|': 'or', '&lt;': 'lt', '&gt;': 'gt', '=':'eq',
    '~': 'not',
}

class VMWriter:
    def __init__(self, output_file):
        self.output_handle = open(output_file, 'w')

    def _write(self, content, tabs=1):
        self.output_handle.write(TAB * tabs + content)

    def write_push(self, segment, index):
        segment = segment.lower()
        self._write(f'push {segment} {index}')

    def write_pop(self, segment, index):
        segment = segment.lower()
        self._write(f'pop {segment} {index}')

    def write_arithmetic(self, command):
        command = OP_SYMBOL_TO_VM_COMMAND_MAPPER[command]
        self._write(command)

    def write_label(self, label):
        self._write(f'label {label}')

    def write_goto(self, label):
        self._write(f'goto {label}', tabs=0)

    def write_if(self, label):
        self._write(f'if-goto {label}')

    def write_call(self, name, nArgs):
        self._write(f'call {name} {nArgs}')

    def write_function(self, name, nLocals):
        self._write(f'function {name} {nLocals}')

    def write_return(self):
        self._write(f'return')

    def close(self):
        self.output_handle.close()
