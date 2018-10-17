IDENTIFIER_KINDS = ['STATIC', 'FIELD', 'ARG', 'VAR']

class SymbolTable:
    def __init__(self):
        self.class_scope = {}

    def start_subroutine(self):
        self.subroutine_scope = {}

    def define(self, name, type_, kind):
        pass

    def var_count(self, kind):
        pass

    def kind_of(self, name):
        pass

    def type_of(self, name):
        pass

    def index_of(self, name):
        pass
