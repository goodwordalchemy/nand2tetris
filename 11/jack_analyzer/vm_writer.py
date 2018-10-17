class VMWriter:
    def __init__(self, output_file):
        self.output_handle = open(output_file, 'w')

    def write_push(self, segment, index):
        pass

    def write_pop(self, segment, index):
        pass

    def write_arithmetic(self, command):
        pass

    def write_label(self, label):
        pass

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

    def write_call(self, name, nArgs):
        pass

    def write_function(self, name, nLocals):
        pass

    def write_return(self)
        pass

    def close(self):
        pass
