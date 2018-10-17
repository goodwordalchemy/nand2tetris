CLASS_IDENTIFIER_KINDS = ['STATIC', 'FIELD']
SUBROUTINE_IDENTIFIER_KINDS = ['ARG', 'VAR']
IDENTIFIER_KINDS = CLASS_IDENTIFIER_KINDS + SUBROUTINE_IDENTIFIER_KINDS


class SymbolTable:
    def __init__(self):
        self.class_scope = {}
        self.start_subroutine()
        self.var_counts = {ik: 0 for ik in IDENTIFIER_KINDS}

    def __contains__(self, name):
        return name in self.subroutine_scope or name in self.class_scope

    def start_subroutine(self):
        self.subroutine_scope = {}

    def define(self, name, type_, kind):
        kind = kind.upper()

        index = self.var_count(kind)
        self.var_counts[kind] += 1

        if kind in CLASS_IDENTIFIER_KINDS:
            scope = self.class_scope
        elif kind in SUBROUTINE_IDENTIFIER_KINDS:
            scope = self.subroutine_scope

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
