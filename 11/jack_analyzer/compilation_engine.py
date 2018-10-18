import functools
import re

from .symbol_table import SymbolTable
from .vm_writer import VMWriter

INDENT_CHAR = '  '
TERMINAL_TAG_PATTERN =  r'^<(\w+?)> (.+?) </\w+>\n$'

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
    def __init__(self, tokenizer, output_filename, vm_output_filename):
        self.tokenizer = tokenizer
        self.tokenizer.advance()
        self.output_handle = open(output_filename, 'w')
        self.recursion_depth = 0

        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(vm_output_filename)

        self.if_counter = 0
        self.while_counter = 0

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

                result = func(self)

                self.recursion_depth -= 1
                self._write('</{}>\n'.format(tagname))

                return result

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

    # @_wrap_output_in_xml_tag('subroutineBody')

    def _compile_subroutine_call(self, n_args=0):
        name = self._compile_identifier() # subroutineName | (className | varName)

        if self._is_symbol() and self._symbol_in('.'):
            if name in self.symbol_table:
                # set this argument if it's in the symbol table.  Otherwise, It's a clasname
                kind = self.kind_of(name)
                index = self.index_of(name)
                self._write_identifier_string(kind, 'used', kind, index)
                self.write_push(kind, index)
                n_args += 1
            else:
                self._write_identifier_string('class', 'used', False, False)

            self._compile_symbol() # .
            name += '.' + self._compile_identifier() # subroutineName
            self._write_identifier_string('subroutine', 'used', False, False)

        self._compile_symbol() # (
        n_args += self.compile_expression_list()
        self._compile_symbol() # )

        self.vm_writer.write_call(name, n_args)

    @_wrap_output_in_xml_tag('class')
    def compile_class(self):
        # Tokenzizer is already advanced, like in other methods.
        category = self._compile_keyword() # class
        name = self._compile_identifier() # className
        self._write_identifier_string(category, 'defined', False, None)
        self.class_name = name

        self._compile_symbol() # {

        num_fields = 0
        while self._keyword_in(CLASS_VAR_DEC_KEYWORD):
            num_fields += self.compile_class_var_dec()
        self.num_fields = num_fields

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

        num_fields = 1
        while self._is_symbol() and self._symbol_in(','):
            num_fields += 1
            self._compile_symbol() # ','
            name = self._compile_identifier() # varName

            if kind == 'static':
                self.symbol_table.define(name, type_, kind)
                index = self.symbol_table.index_of(name)
            else:
                print('need to handle the field kind')

            self._write_identifier_string(kind, 'defined', kind, index)

        self._compile_symbol() # ';'

        if kind == 'field':
            return num_fields
        else:
            return 0

    @_wrap_output_in_xml_tag('subroutineDec')
    def compile_subroutine(self):
        if not self._keyword_in(SUBROUTINE_KEYWORDS):
            raise Exception('subroutine declarations should be in {}'.format(SUBROUTINE_KEYWORDS))
        self.symbol_table.start_subroutine()
        subroutine_kind = self._compile_keyword()  # ('constructor' | 'function' | 'method')

        if self._is_keyword() and self._keyword_in('void'):
            self._compile_keyword() # void
            type_ = None
        else:
            type_ = self._compile_type()

        name = self._compile_identifier() # subroutineName
        if subroutine_kind in ['constructor', 'function']:
            name = self.class_name + '.' + name
        self._write_identifier_string('subroutine', 'defined', False, None)

        self._compile_symbol() # (
        self.compile_parameter_list()
        self._compile_symbol() # )

        self._compile_symbol() # {

        num_locals = 0
        while self._is_keyword() and self._keyword_in('var'):
            num_vars_declared = self.compile_var_dec()
            num_locals += num_vars_declared

        if subroutine_kind in ['constructor', 'function']:
            self.vm_writer.write_function(name, num_locals)
        else: # compiling a method
            self.vm_writer.write_function(name, num_locals + 1)

        if subroutine_kind == 'constructor':
            self.vm_writer.write_call('Memory.alloc', self.num_fields)
            self.vm_writer.write_pop('this', 0)

        if not type_:
            print('compile_subroutine...pushing constant 0 for void method')
            self.vm_writer.write_push('constant', 0)

        self.compile_statements()
        self._compile_symbol() # }

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
        num_vars_declared = 1

        kind = self._compile_keyword() # var
        type_ = self._compile_type()

        name = self._compile_identifier() # varName
        self.symbol_table.define(name, type_, kind)
        st_index = self.symbol_table.index_of(name)
        self._write_identifier_string(kind, 'defined', kind, st_index)

        while self._is_symbol() and self._symbol_in(','):
            num_vars_declared += 1

            self._compile_symbol() # ,
            name = self._compile_identifier() # varName
            self.symbol_table.define(name, type_, kind)
            st_index = self.symbol_table.index_of(name)
            self._write_identifier_string(kind, 'defined', kind, st_index)

        self._compile_symbol() # ;


        return num_vars_declared

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

        self.vm_writer.write_pop('temp', 0)

    @_wrap_output_in_xml_tag('letStatement')
    def compile_let(self):
        self._compile_keyword() # let

        name = self._compile_identifier() # varName
        kind = self.symbol_table.kind_of(name)
        index = self.symbol_table.index_of(name)
        print(f'in let statement: kind: {kind}, name: {name}, index: {index}')
        self._write_identifier_string(kind, 'used', kind, index)

        array_entry = False
        if self._is_symbol() and self._symbol_in('['):
            array_entry = True
            self._compile_symbol() # [
            result = self.compile_expression()
            self._compile_symbol() # ]
            self.vm_writer.write_arithmetic('+')
            self.vm_writer.write_pop('pointer', 1)

        self._compile_symbol() # =
        self.compile_expression()

        if array_entry:
            self.vm_writer.write_pop('that', 0)
        else:
            self.vm_writer.write_pop(kind, index)

        self._compile_symbol() # ;

    @_wrap_output_in_xml_tag('whileStatement')
    def compile_while(self):
        self._compile_keyword() # while
        self.vm_writer.write_label(f'WHILE_START{self.while_counter}')
        self._compile_symbol() # (
        self.compile_expression()
        self._compile_symbol() # )
        self.vm_writer.write_arithmetic('~')
        self.vm_writer.write_if(f'WHILE_END{self.while_counter}')

        self._compile_symbol() # {
        self.compile_statements()
        self.vm_writer.write_goto(f'WHILE_START{self.while_counter}')
        self.vm_writer.write_label(f'WHILE_END{self.while_counter}')
        self._compile_symbol() # }


    @_wrap_output_in_xml_tag('returnStatement')
    def compile_return(self):
        self._compile_keyword() # return

        if not self._is_symbol():
            self.compile_expression()

        self.vm_writer.write_return()
        self._compile_symbol() # ;

    @_wrap_output_in_xml_tag('ifStatement')
    def compile_if(self):
        self._compile_keyword() # if
        self._compile_symbol() # (
        self.compile_expression()
        self.vm_writer.write_if(f'IF_TRUE{self.if_counter}')
        self._compile_symbol() # )

        self._compile_symbol() # {
        self.vm_writer.write_goto(f'IF_FALSE{self.if_counter}')
        self.vm_writer.write_label(f'IF_TRUE{self.if_counter}')
        self.compile_statements()
        self._compile_symbol() # }

        if self._is_keyword() and self._keyword_in('else'):
            self.vm_writer.write_label(f'IF_FALSE{self.if_counter}')
            self._compile_keyword() # else
            self._compile_symbol() # {
            self.compile_statements()
            self._compile_symbol() # }

        self.if_counter += 1

    @_wrap_output_in_xml_tag('expression')
    def compile_expression(self):
        self.compile_term()

        while self._is_symbol() and self._symbol_in(OP_SYMBOLS):
            symbol = self._compile_symbol() # op
            self.compile_term()
            self.vm_writer.write_arithmetic(symbol)

    @_wrap_output_in_xml_tag('term')
    def compile_term(self):
        if self._is_int_const():
            value = self._compile_int()
            self.vm_writer.write_push('constant', value)

        elif self._is_string_const():
            string = self._compile_string()

            self.vm_writer.write_push('constant', len(string))
            self.vm_writer.write_call('String.new', 1)

            for letter in string:
                self.vm_writer.write_push('constant', ord(letter))
                self.vm_writer.write_call('String.appendChar', 2)

        elif self._is_keyword() and self._keyword_in(KEYWORD_CONSANT_KEYWORDS):
            kw = self._compile_keyword()

            if kw in ['null', 'false']:
                self.vm_writer.push('constant', 0)
            else:
                self.vm_writer.push('constant', -1)

        elif self._is_symbol() and self._symbol_in('('): # ( expression )
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()

        elif self._is_symbol() and self._symbol_in(UNARY_OP_KEYWORDS):
            symbol = self._compile_symbol() # unaryOp
            self.vm_writer.write_arithmetic(symbol)
            self.compile_term()

        # varName |
        # varName[expression] |
        # subroutineCall: subroutineName ( expressionList ) |
        #                 (className | varName) . subroutineName ( expressionList )
        elif self._is_identifier():
            print(f'compile_term...correctly identified identifier')
            name = self._compile_identifier() # subroutineName | className | varName
            kind = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            print(f'compile_term...symbol table lookup: name: {name}, kind: {kind}, index: {index}')
            self._write_identifier_string(kind, 'used', kind, index)


            if self._is_symbol() and self._symbol_in('['):
                self.vm_writer.write_push(kind, index)
                self._compile_symbol() # [
                self.compile_expression() # expression
                self._compile_symbol() # ]
                self.vm_writer.write_arithmetic('+')
                self.vm_writer.write_pop('pointer', 1)

            elif self._is_symbol() and self._symbol_in('.'):
                print(f'compile term...correctly identified class membership (.)')

                #### This is probably wrong, though I might have to do something like this
                #### to look up a field.
                # self.vm_writer.write_push(kind, index)
                ####

                self._compile_symbol() # .

                # subroutineName ( expressionList )
                name += '.' + self._compile_identifier()

                self._compile_symbol() # (
                n_args = self.compile_expression_list()
                self._compile_symbol() # )

                self.vm_writer.write_call(name, n_args)
            else:
                self.vm_writer.write_push(kind, index)

        else:
            raise Exception('Could not parse terminal')

    @_wrap_output_in_xml_tag('expressionList')
    def compile_expression_list(self):
        if self._is_symbol() and self._symbol_in(')'):
            return

        self.compile_expression()

        num_expressions = 1
        while self._is_symbol() and self._symbol_in(','):
            num_expressions += 1
            self._compile_symbol()
            self.compile_expression()

        return num_expressions
