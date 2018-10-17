import functools
import re

from .symbol_table import SymbolTable
from .vm_writer import VMWriter

INDENT_CHAR = '  '
TERMINAL_TAG_PATTERN =  r'^<(\w+?)> (\S+?) </\w+>\n$'

def _xml_tag(tagname, inner):
    return '<{tagname}> {inner} </{tagname}>\n'.format(
        tagname=tagname, inner=inner
    )

def _get_terminal_value(tag):
    match = re.match(TERMINAL_TAG_PATTERN, tag)

    if not match:
        raise Exception(f'this function should only be called on terminal tags: {tag}')

    value = match.group(2)

    return value

def _xml_tag_list(tagname, inner_list):
    return [_xml_tag(tagname, il) for il in inner_list]


CLASS_VAR_DEC_KEYWORD = ['static', 'field']
KEYWORD_CONSANT_KEYWORDS = ['true', 'false', 'null', 'this']
OP_SYMBOLS = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
STATEMENT_KEYWORDS = ['let', 'if', 'while', 'do', 'return']
SUBROUTINE_KEYWORDS = ['constructor', 'function', 'method']
UNARY_OP_KEYWORDS = ['-', '~']

class CompilationEngine:
    def __init__(self, tokenizer, output_filename):
        self.tokenizer = tokenizer
        self.tokenizer.advance()
        self.output_handle = open(output_filename, 'w')
        self.recursion_depth = 0

        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(self.output_handle)

    def _print_current_token(self, message=''):
        print(message, self.tokenizer.current_token)

    def _get_indent(self):
        return INDENT_CHAR * self.recursion_depth

    def _wrap_output_in_xml_tag(tagname):
        def decorator_wrap_output(func):
            @functools.wraps(func)
            def wrap(self):
                self._write('<{}>\n'.format(tagname))
                self.recursion_depth += 1

                func(self)

                self.recursion_depth -= 1
                self._write('</{}>\n'.format(tagname))

            return wrap
        return decorator_wrap_output

    def _write(self, content):
        self.output_handle.write(self._get_indent() + content)

    def _write_identifier_string(self, category, defined_or_used, kind, st_index):
        self._write(f'\tcategory: {category}\n')
        self._write(f'\tdefined or used?: {defined_or_used}\n')
        self._write(f'\trepresents one of [var, argument, static, field]: {kind}\n')
        self._write(f'\tsymbol table index: {st_index}\n')

    def _get_identifier(self):
        return self.tokenizer.identifier()

    def _get_symbol(self):
        return self.tokenizer.symbol()

    def _get_keyword(self):
        return self.tokenizer.key_word()

    def _get_int_const(self):
        return self.tokenizer.int_val()

    def _get_string_const(self):
        return self.tokenizer.string_val()

    def _is_identifier(self):
        return self.tokenizer.token_type() == 'IDENTIFIER'

    def _is_symbol(self):
        return self.tokenizer.token_type() == 'SYMBOL'

    def _is_keyword(self):
        return self.tokenizer.token_type() == 'KEYWORD'

    def _is_int_const(self):
        return self.tokenizer.token_type() == 'INT_CONST'

    def _is_string_const(self):
        return self.tokenizer.token_type() == 'STRING_CONST'

    def _keyword_in(self, token_list):
        if not isinstance(token_list, list):
            token_list = [token_list]

        token_list = _xml_tag_list('keyword', token_list)

        return ((self.tokenizer.token_type() == 'KEYWORD') and
                (self.tokenizer.key_word() in token_list))

    def _symbol_in(self, token_list):
        if not isinstance(token_list, list):
            token_list = [token_list]

        token_list = _xml_tag_list('symbol', token_list)

        return ((self.tokenizer.token_type() == 'SYMBOL') and
                (self.tokenizer.symbol() in token_list))

    def _compile_int(self):
        int_value = self._get_int_const()
        self._write(int_value)
        self.tokenizer.advance()

        return _get_terminal_value(int_value)

    def _compile_string(self):
        string_value = self._get_string_const()
        self._write(string_value)
        self.tokenizer.advance()

        return _get_terminal_value(string_value)

    def _compile_identifier(self):
        identifier_value = self.tokenizer.identifier()
        self._write(identifier_value)
        self.tokenizer.advance()

        return _get_terminal_value(identifier_value)

    def _compile_keyword(self):
        keyword_value = self.tokenizer.key_word()
        self._write(keyword_value)
        self.tokenizer.advance()

        return _get_terminal_value(keyword_value)

    def _compile_symbol(self):
        symbol_value = self.tokenizer.symbol()
        self._write(symbol_value)
        self.tokenizer.advance()

        return _get_terminal_value(symbol_value)

    def _compile_type(self):
        if self._is_keyword() and self._keyword_in(['int', 'char', 'boolean']):
            type_ = self._compile_keyword() # built-in type

        elif self._is_identifier():
            name = type_ = self._compile_identifier() # custom type
            self._write_identifier_string('class', 'used', False, False)

        else:
            raise Exception('Error compiling type')

        return type_

    @_wrap_output_in_xml_tag('subroutineBody')
    def compile_subroutine_body(self):
        self._compile_symbol() # {

        while self._is_keyword() and self._keyword_in('var'):
            self.compile_var_dec()

        self.compile_statements()
        self._compile_symbol() # }

    def _compile_subroutine_call(self):
        name = self._compile_identifier() # subroutineName | (className | varName)

        if self._is_symbol() and self._symbol_in('.'):
            if name in self.symbol_table:
                kind = self.kind_of(name)
                index = self.index_of(name)
                self._write_identifier_string(kind, 'used', kind, index)
            else:
                self._write_identifier_string('class', 'used', False, False)

            self._compile_symbol() # .
            self._compile_identifier() # subroutineName
            self._write_identifier_string('subroutine', 'used', False, False)

        self._compile_symbol() # (
        self.compile_expression_list()
        self._compile_symbol() # )

    @_wrap_output_in_xml_tag('class')
    def compile_class(self):
        # Tokenzizer is already advanced, like in other methods.
        category = self._compile_keyword() # class
        name = self._compile_identifier() # className
        self._write_identifier_string(category, 'defined', False, None)
        self._compile_symbol() # {

        while self._keyword_in(CLASS_VAR_DEC_KEYWORD):
            self.compile_class_var_dec()

        while self._keyword_in(SUBROUTINE_KEYWORDS):
            self.compile_subroutine()

        # NOTE: didn't use compile symbol because advance would cause an error
        self._write(self.tokenizer.symbol()) # }

    @_wrap_output_in_xml_tag('classVarDec')
    def compile_class_var_dec(self):
        if not self._keyword_in(['static', 'field']):
            raise Exception('class variable declarations must start with "static" or "field"')

        kind = self._compile_keyword() # field or static
        type_ = self._compile_type() # type
        name = self._compile_identifier() # varName
        self.symbol_table.define(name, type_, kind)
        index = self.symbol_table.index_of(name)
        self._write_identifier_string(kind, 'defined', kind, index)

        while self._is_symbol() and self._symbol_in(','):
            self._compile_symbol() # ','
            name = self._compile_identifier() # varName
            self.symbol_table.define(name, type_, kind)
            index = self.symbol_table.index_of(name)
            self._write_identifier_string(kind, 'defined', kind, index)

        self._compile_symbol() # ';'

    @_wrap_output_in_xml_tag('subroutineDec')
    def compile_subroutine(self):
        if not self._keyword_in(SUBROUTINE_KEYWORDS):
            raise Exception('subroutine declarations should be in {}'.format(SUBROUTINE_KEYWORDS))
        self.symbol_table.start_subroutine()
        self._compile_keyword()  # ('constructor' | 'function' | 'method')

        if self._is_keyword() and self._keyword_in('void'):
            self._compile_keyword() # void
            type_ = None
        else:
            type_ = self._compile_type()

        name = self._compile_identifier() # subroutineName
        self._write_identifier_string('subroutine', 'defined', False, None)

        self._compile_symbol() # (
        self.compile_parameter_list()
        self._compile_symbol() # )

        self.compile_subroutine_body()

    @_wrap_output_in_xml_tag('parameterList')
    def compile_parameter_list(self):
        while self._is_keyword() or self._is_identifier():

            if self._is_keyword():
                type_ = self._compile_keyword() # built-in type

            elif self._is_identifier():
                name = self._compile_identifier() # custom type
                self._write_identifier_string('class', 'used', False, False)
                type_ = self.symbol_table.type_of(name)

            name = self._compile_identifier() # varName
            self.symbol_table.define(name, type_, 'ARG')
            index = self.symbol_table.index_of(name)
            self._write_identifier_string('argument', 'defined', 'argument', index)

            if self._is_symbol() and self._symbol_in(','):
                self._compile_symbol()

    @_wrap_output_in_xml_tag('varDec')
    def compile_var_dec(self):
        if not self._keyword_in('var'):
            raise Exception('variable declaration must start with "var"')
        kind = self._compile_keyword() # var
        type_ = self._compile_type()

        name = self._compile_identifier() # varName
        self.symbol_table.define(name, type_, kind)
        st_index = self.symbol_table.index_of(name)
        self._write_identifier_string(kind, 'defined', kind, st_index)

        while self._is_symbol() and self._symbol_in(','):
            self._compile_symbol() # ,
            self._compile_identifier() # varName
            self.symbol_table.define(name, type_, kind)
            st_index = self.symbol_table.index_of(name)
            self._write_identifier_string(kind, 'defined', kind, st_index)

        self._compile_symbol() # ;

    @_wrap_output_in_xml_tag('statements')
    def compile_statements(self):
        while self._is_keyword() and self._keyword_in(STATEMENT_KEYWORDS):
            if self._keyword_in('let'):
                self.compile_let()

            elif self._keyword_in('if'):
                self.compile_if()

            elif self._keyword_in('while'):
                self.compile_while()

            elif self._keyword_in('do'):
                self.compile_do()

            elif self._keyword_in('return'):
                self.compile_return()

            else:
                raise Exception('unknown statement keyword')

    @_wrap_output_in_xml_tag('doStatement')
    def compile_do(self):
        self._compile_keyword() # do
        self._compile_subroutine_call()
        self._compile_symbol() # ;

    @_wrap_output_in_xml_tag('letStatement')
    def compile_let(self):
        self._compile_keyword() # let

        name = self._compile_identifier() # varName
        kind = self.symbol_table.kind_of(name)
        index = self.symbol_table.index_of(name)
        self._write_identifier_string(kind, 'used', kind, index)

        if self._is_symbol() and self._symbol_in('['):
            self._compile_symbol() # [
            self.compile_expression()
            self._compile_symbol() # ]

        self._compile_symbol() # =
        self.compile_expression()
        self._compile_symbol() # ;

    @_wrap_output_in_xml_tag('whileStatement')
    def compile_while(self):
        self._compile_keyword() # while
        self._compile_symbol() # (
        self.compile_expression()
        self._compile_symbol() # )

        self._compile_symbol() # {
        self.compile_statements()
        self._compile_symbol() # }

    @_wrap_output_in_xml_tag('returnStatement')
    def compile_return(self):
        self._compile_keyword() # return

        if not self._is_symbol():
            self.compile_expression()

        self._compile_symbol() # ;

    @_wrap_output_in_xml_tag('ifStatement')
    def compile_if(self):
        self._compile_keyword() # if
        self._compile_symbol() # (
        self.compile_expression()
        self._compile_symbol() # )

        self._compile_symbol() # {
        self.compile_statements()
        self._compile_symbol() # }

        if self._is_keyword() and self._keyword_in('else'):
            self._compile_keyword() # else
            self._compile_symbol() # {
            self.compile_statements()
            self._compile_symbol() # }

    @_wrap_output_in_xml_tag('expression')
    def compile_expression(self):
        self.compile_term()

        while self._is_symbol() and self._symbol_in(OP_SYMBOLS):
            self._compile_symbol() # op
            self.compile_term()


    @_wrap_output_in_xml_tag('term')
    def compile_term(self):
        if self._is_int_const():
            self._compile_int()

        elif self._is_string_const():
            self._compile_string()

        elif self._is_keyword() and self._keyword_in(KEYWORD_CONSANT_KEYWORDS):
            self._compile_keyword()

        elif self._is_symbol() and self._symbol_in('('): # ( expression )
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()

        elif self._is_symbol() and self._symbol_in(UNARY_OP_KEYWORDS):
            self._compile_symbol() # unaryOp
            self.compile_term()

        # varName |
        # varName[expression] |
        # subroutineCall: subroutineName ( expressionList ) |
        #                 (className | varName) . subroutineName ( expressionList )
        elif self._is_identifier():
            name = self._compile_identifier() # subroutineName | className | varName
            kind = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            self._write_identifier_string(kind, 'used', kind, index)

            if self._is_symbol() and self._symbol_in('['):
                self._compile_symbol() # [
                self.compile_expression() # expression
                self._compile_symbol() # ]

            elif self._is_symbol() and self._symbol_in('.'):
                self._compile_symbol() # .
                self._compile_subroutine_call()  # subroutineName ( expressionList )

        else:
            raise Exception('Could not parse terminal')

    @_wrap_output_in_xml_tag('expressionList')
    def compile_expression_list(self):
        if self._is_symbol() and self._symbol_in(')'):
            return

        self.compile_expression()

        while self._is_symbol() and self._symbol_in(','):
            self._compile_symbol()
            self.compile_expression()
