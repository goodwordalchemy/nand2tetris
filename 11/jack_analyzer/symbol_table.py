CLASS_IDENTIFIER_KINDS = ['STATIC', 'FIELD']
SUBROUTINE_IDENTIFIER_KINDS = ['ARG', 'VAR']
IDENTIFIER_KINDS = CLASS_IDENTIFIER_KINDS + SUBROUTINE_IDENTIFIER_KINDS


class SymbolTable:
    def __init__(self):
        self.class_scope = {}
        self.var_counts = {ik: 0 for ik in IDENTIFIER_KINDS}
        self.start_subroutine()

    def __contains__(self, name):
        return name in self.subroutine_scope or name in self.class_scope

    def start_subroutine(self):
        self.subroutine_scope = {}

        for si in SUBROUTINE_IDENTIFIER_KINDS:
            self.var_counts[si] = 0

    def define(self, name, type_, kind):
        kind = kind.upper()

        index = self.var_count(kind)
        self.var_counts[kind] += 1

        if kind == 'STATIC':
            scope = self.class_scope
        elif kind in SUBROUTINE_IDENTIFIER_KINDS:
            scope = self.subroutine_scope
        else:
            raise Exception('identifiers of kind, "{kind}" should not be included in symbol table')

        scope[name] = {'type': type_, 'kind': kind, 'index': index}

    def var_count(self, kind):
        return self.var_counts[kind]

    def _get_scope_property(self, name, prop):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][prop]

        if name in self.class_scope:
            return self.class_scope[name][prop]

        return None

    def kind_of(self, name):
        kind = self._get_scope_property(name, 'kind') or 'NONE'

        return kind

    def type_of(self, name):
        type_ = self._get_scope_property(name, 'type')

        return type_

    def index_of(self, name):
        index = self._get_scope_property(name, 'index')

        return index
