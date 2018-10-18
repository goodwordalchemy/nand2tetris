TAB = '\t'

OP_SYMBOL_TO_VM_COMMAND_MAPPER = {
    '+': 'add', '-': 'sub', '*': 'call Math.multiply 2', '/': 'call Math.divide 2',
    '&amp;': 'and', '|': 'or', '&lt;': 'lt', '&gt;': 'gt', '=':'eq',
}
UNARY_OP_SYMBOL_TO_CM_COMMAND_MAPPER = {
    '-': 'neg', '~': 'not'
}
KIND_TO_SEGMENT_MAPPER = {
    'VAR': 'local', 'ARG': 'argument', 'STATIC': 'static', 'field': 'this'
}

class VMWriter:
    def __init__(self, output_file):
        self.output_handle = open(output_file, 'w')

    def _write(self, content, tabs=0):
        self.output_handle.write(TAB * tabs + content + '\n')

    def write_push(self, segment, index):
        segment = KIND_TO_SEGMENT_MAPPER.get(segment, segment)
        segment = segment.lower()

        self._write(f'push {segment} {index}')

    def write_pop(self, segment, index):
        segment = KIND_TO_SEGMENT_MAPPER.get(segment, segment)
        segment = segment.lower()

        self._write(f'pop {segment} {index}')

    def write_arithmetic(self, command):
        self._write(command)

    def write_label(self, label):
        self._write(f'label {label}', tabs=0)

    def write_goto(self, label):
        self._write(f'goto {label}')

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
