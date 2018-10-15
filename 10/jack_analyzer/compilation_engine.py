import functools

def _xml_tag(tagname, inner):
    return '<{tagname}> {inner} </{tagname}>\n'.format(
        tagname=tagname, inner=inner
    )

def _xml_tag_list(tagname, inner_list):
    return [_xml_tag(tagname, il) for il in inner_list]

CLASS_VAR_DEC_KEYWORD = ['static', 'field']
KEYWORD_CONSANT_KEYWORDS = ['true', 'false', 'null', 'this']
OP_SYMBOLS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
STATEMENT_KEYWORDS = ['let', 'if', 'while', 'do', 'return']
SUBROUTINE_KEYWORDS = ['constructor', 'function', 'method']
UNARY_OP_KEYWORDS = ['-', '~']

class CompilationEngine:
    def __init__(self, tokenizer, output_filename):
        self.tokenizer = tokenizer
        self.tokenizer.advance()
        self.output_handle = open(output_filename, 'w')

    def _wrap_output_in_xml_tag(tagname):
        def decorator_wrap_output(func):
            @functools.wraps(func)
            def wrap(self):
                self._write('<{}>\n'.format(tagname))
                func(self)
                self._write('</{}>\n'.format(tagname))

            return wrap
        return decorator_wrap_output

    def _write(self, content):
        self.output_handle.write(content)

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
        self._write(self.tokenizer.int_val())
        self.tokenizer.advance()

    def _compile_string(self):
        self._write(self.tokenizer.string_val())
        self.tokenizer.advance()

    def _compile_identifier(self):
        self._write(self.tokenizer.identifier())
        self.tokenizer.advance()

    def _compile_keyword(self):
        self._write(self.tokenizer.key_word())
        self.tokenizer.advance()

    def _compile_symbol(self):
        self._write(self.tokenizer.symbol())
        self.tokenizer.advance()

    def _compile_type(self):
        if self._is_keyword(self) and _keyword_in(['int', 'char', 'boolean']):
            self._compile_keyword() # built-in type

        elif self.tokenizer._is_identifier():
            self._compile_identifier() # custom type

        else:
            raise Exception('Error compiling type')

    def _compile_subroutine_body()
        self._compile_symbol() # {

        while self._is_keyword() and self._keyword_in('var'):
            self.compile_var_dec()

        self.compile_statements()
        self._compile_symbol() # }

    def _compile_subroutine_call(self):
        self._compile_identifier() # subroutineName | (className | varName)

        if self._is_symbol() and self._symbol_in('.'):
            self._compile_symbol() # .
            self._compile_identifier() # subroutineName

        self._compile_symbol() # (
        self.compile_expression_list()
        self._compile_symbol() # )

    @_wrap_output_in_xml_tag('class')
    def compile_class(self):
        # Tokenzizer is already advanced, like in other methods.
        self._compile_keyword() # class
        self._compile_identifier() # className
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
        self._compile_keyword() # field or static

        self._compile_type() # type

        self._compile_identifier() # varName

        while self._is_symbol() and self._symbol_in(','):
            self._compile_symbol() # ','
            self._compile_identifier() # varName

        self._compile_symbol() # ';'

    @_wrap_output_in_xml_tag('subroutineDec')
    def compile_subroutine(self):
        if not self._keyword_in(SUBROUTINE_KEYWORDS):
            raise Exception('subroutine declarations should be in {}'.format(SUBROUTINE_KEYWORDS)
        self._compile_keyword()  # ('constructor' | 'function' | 'method')

        if self._is_keyword() and self._keyword_in('void'):
            self._compile_keyword() # void
        else:
            self._compile_type()

        self._compile_identifier() # subroutineName
        self._compile_symbol() # (
        self.compile_parameter_list()
        self._compile_symbol() # )
        self._compile_symbol() # {

        self._compile_subroutine_body()

    @_wrap_output_in_xml_tag('parameterList')
    def compile_parameter_list(self):
        while ((self.tokenizer.token_type() == 'KEYWORD') or
               (self.tokenizer.token_type() == 'IDENTIFIER')):

            if self.tokenizer.token_type() == 'KEYWORD':
                self._write(self.tokenizer.key_word()) # built-in type

            elif self.tokenizer.token_type() == 'IDENTIFIER':
                self._write(self.tokenizer.identifier()) # custom type

            self.tokenizer.advance()
            self._write(self.tokenizer.identifier()) # varName

            self.tokenizer.advance()

            if ((self.tokenizer.token_type() == 'SYMBOL') and
                (self.tokenizer.symbol() == _xml_tag('symbol', ','))):
                self._write(self.tokenizer.symbol()) # ","
                self.tokenizer.advance()

    @_wrap_output_in_xml_tag('varDec')
    def compile_var_dec(self):
        if not self._keyword_in('var'):
            raise Exception('variable declaration must start with "var"')
        self._compile_keyword() # var

        self._compile_type()

        self._compile_identifier() # varName

        while self._is_symbol() and self._symbol_in(','):
            self._compile_symbol() # ,
            self._compile_identifier() # varName

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

    @_wrap_output_in_xml_tag('letStatment')
    def compile_let(self):
        self._compile_keyword() # let
        self._compile_identifier() # varName

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

        if self._is_symbol() and self._symbol_in(OP_SYMBOLS):
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
            self._compile_identifier() # subroutineName | className | varName

            if self._is_symbol() and self._symbol_in('['):
                self._compile_symbol() # [
                self.compile_expression() # expression
                self._compile_symbol() # ]

            elif self.is_symbol() and self._symbol_in('.'):
                self._compile_symbol() # .
                self._compile_subroutine_call()  # subroutineName ( expressionList )

        else:
            raise Exception('Could not parse terminal')

    @_wrap_output_in_xml_tag('expressionList')
    def compile_expression_list(self):
        self.compile_expression()

        while self._is_symbol() and self._symbol_in(','):
            self._compile_symbol()
            self.compile_expression()
