import functools

def _xml_tag(tagname, inner):
    return '<{tagname}> {inner} </{tagname}>\n'.format(
        tagname=tagname, inner=inner
    )

CLASS_VAR_DEC_KEYWORD_TOKENS = [_xml_tag('keyword', kw) for kw in ['static', 'field']]
KEYWORD_CONSTANT_TOKENS = [_xml_tag('keyword', kw) for kw in ['true', 'false', 'null', 'this']]
OP_SYMBOL_TOKENS = [_xml_tag('symbol', s) for s in ['+', '-', '*', '/', '&', '|', '<', '>', '=']]
STATEMENT_KEYWORD_TOKENS = [_xml_tag('keyword', kw) for kw in ['let', 'if', 'while', 'do', 'return']]
SUBROUTINE_DEC_KEYWORD_TOKENS = [_xml_tag('keyword', kw) for kw in ['constructor', 'function', 'method']]
UNARY_OP_KEYWORD_TOKENS = [_xml_tag('symbol', s) for s in ['-', '~']]

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

    @_wrap_output_in_xml_tag('class')
    def compile_class(self):
        # Tokenzizer is already advanced, like in other methods.
        self._write(self.tokenizer.key_word()) # "class"

        self.tokenizer.advance()
        self._write(self.tokenizer.identifier()) # className

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol()) # {

        self.tokenizer.advance()
        print('token before class var decs: {}'.format(self.tokenizer.current_token))
        while ((self.tokenizer.token_type() == 'KEYWORD') and
               (self.tokenizer.key_word() in CLASS_VAR_DEC_KEYWORD_TOKENS)):
            self.compile_class_var_dec()
            self.tokenizer.advance()

        print('token before subroutine decs: {}'.format(self.tokenizer.current_token))
        while ((self.tokenizer.token_type() == 'KEYWORD') and
               (self.tokenizer.key_word() in SUBROUTINE_DEC_KEYWORD_TOKENS)):
            self.compile_subroutine()
            self.tokenizer.advance()

        self._write(self.tokenizer.symbol()) # }

    @_wrap_output_in_xml_tag('classVarDec')
    def compile_class_var_dec(self):
        self._write(self.tokenizer.key_word())

        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'KEYWORD':
            self._write(self.tokenizer.key_word()) # built-in type
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            self._write(self.tokenizer.identifier()) # custom type
        else:
            raise Exception('Error Parsing type')

        self.tokenizer.advance()
        self._write(self.tokenizer.identifier()) # varName

        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'SYMBOL':
            while self.tokenizer.symbol() == _xml_tag('symbol', ','):
                self._write(self.tokenizer.symbol())

                self.tokenizer.advance()
                self._write(self.tokenizer.identifier())

                self.tokenizer.advance()

        self._write(self.tokenizer.symbol())

    @_wrap_output_in_xml_tag('subroutineDec')
    def compile_subroutine(self):
        self._write(self.tokenizer.key_word())  # ('constructor' | 'function' | 'method')

        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'KEYWORD':
            self._write(self.tokenizer.key_word()) # built-in type
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            self._write(self.tokenizer.identifier()) # custom type
        else:
            raise Exception('Error Parsing type')

        self.tokenizer.advance()
        self._write(self.tokenizer.identifier()) # subroutineName

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol()) # "("

        self.tokenizer.advance()
        self.compile_parameter_list()

        self._write(self.tokenizer.symbol()) # ")"

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol()) # "{"

        # subroutine body
        self.tokenizer.advance()
        while ((self.tokenizer.token_type() == 'KEYWORD') and
               (self.tokenizer.key_word() == _xml_tag('keyword', 'var'))):
            self.compile_var_dec()
            self.tokenizer.advance()

        self.compile_statements()

        self._write(self.tokenizer.symbol()) # "}"

    def _compile_subroutine_call(self):
        while (self.tokenizer.token_type() == 'IDENTIFIER'):
            self._write(self.tokenizer.identifier()) # subroutineName or className or varName

            # NOTE: This may be more recursion than required.
            self.tokenizer.advance()
            if ((self.tokenizer.token_type() == 'SYMBOL') and
                (self.tokenizer.symbol() == _xml_tag('symbol', '.'))):

                self._write(self.tokenizer.symbol()) # "."

                self.tokenizer.advance()
                self._write(self.tokenizer.identifier()) # subroutineName

                self.tokenizer.advance()

        print('in subroutine call.  this should a big (... {}'.format(self.tokenizer.current_token))
        self._write(self.tokenizer.symbol())  # (

        self.tokenizer.advance()
        self.compile_expression_list()

        print('in subroutine call.  this should a big )... {}'.format(self.tokenizer.current_token))
        self._write(self.tokenizer.symbol())  # )

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
        self._write(self.tokenizer.key_word()) #  var

        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'KEYWORD':
            self._write(self.tokenizer.key_word()) # built-in type
        elif self.tokenizer.token_type() == 'IDENTIFIER':
            self._write(self.tokenizer.identifier()) # custom type
        else:
            raise Exception('Error Parsing type')

        self.tokenizer.advance()
        self._write(self.tokenizer.identifier()) # varName

        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'SYMBOL':
            while self.tokenizer.symbol() == _xml_tag('symbol', ','):
                self._write(self.tokenizer.symbol())

                self.tokenizer.advance()
                self._write(self.tokenizer.identifier())

                self.tokenizer.advance()

        self._write(self.tokenizer.symbol())

    @_wrap_output_in_xml_tag('statements')
    def compile_statements(self):
        #  NOTE: compiling statements advances the parser
        while ((self.tokenizer.token_type() == 'KEYWORD') and
               (self.tokenizer.key_word() in STATEMENT_KEYWORD_TOKENS)):

            print('in compile statments: {}'.format(self.tokenizer.current_token))
            if self.tokenizer.key_word() == _xml_tag('keyword', 'let'):
                self.compile_let()

            elif self.tokenizer.key_word() == _xml_tag('keyword', 'if'):
                self.compile_if()

            elif self.tokenizer.key_word() == _xml_tag('keyword', 'while'):
                self.compile_while()

            elif self.tokenizer.key_word() == _xml_tag('keyword', 'do'):
                self.compile_do()

            elif self.tokenizer.key_word() == _xml_tag('keyword', 'return'):
                self.compile_return()
        print('in compile statments: {}'.format(self.tokenizer.current_token))

    @_wrap_output_in_xml_tag('doStatement')
    def compile_do(self):
        self._write(self.tokenizer.key_word()) # "do"

        self.tokenizer.advance()
        self._compile_subroutine_call()

        print('in compile do: {}'.format(self.tokenizer.current_token))
        self.tokenizer.advance()
        print('in compile do, this should be an ";": {}'.format(self.tokenizer.current_token))
        self._write(self.tokenizer.symbol()) # ";"

        self.tokenizer.advance()

    @_wrap_output_in_xml_tag('letStatment')
    def compile_let(self):
        self._write(self.tokenizer.key_word()) # "let"

        #TODO: change this to _compile square_bracket variable
        self.tokenizer.advance()
        self._write(self.tokenizer.identifier())  # varName

        self.tokenizer.advance()
        if ((self.tokenizer.token_type() == 'symbol') and
            (self.tokenizer.symbol() == _xml_tag('['))):

            self._write(self.tokenizer.symbol())  # [

            self.compile_expression()

            self.tokenizer.advance()
            self._write(self.tokenizer.symbol())  # ]

            self.tokenizer.advance()

        self._write(self.tokenizer.symbol())  # =

        self.tokenizer.advance()
        self.compile_expression()

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # ;

        self.tokenizer.advance()

    @_wrap_output_in_xml_tag('whileStatement')
    def compile_while(self):
        self._write(self.tokenizer.key_word()) # "while"

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # (

        self.tokenizer.advance()
        self.compile_expression()

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # )

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # {

        self.tokenizer.advance()
        self.compile_statements()

        self._write(self.tokenizer.symbol())  # }

        self.tokenizer.advance()

    @_wrap_output_in_xml_tag('returnStatement')
    def compile_return(self):
        self._write(self.tokenizer.key_word()) # "return"

        self.tokenizer.advance()
        if not self.tokenizer.token_type() == 'SYMBOL':
            self.compile_expression()
            self.tokenizer.advance()

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # ;

        self.tokenizer.advance()

    @_wrap_output_in_xml_tag('ifStatement')
    def compile_if(self):
        self._write(self.tokenizer.key_word()) # "if"

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # (

        self.tokenizer.advance()
        self.compile_expression()

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # )

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol())  # {

        self.tokenizer.advance()
        self.compile_statements()

        self._write(self.tokenizer.symbol())  # }

        self.tokenizer.advance()
        if ((self.tokenizer.token_type() == 'KEYWORD') and
            (self.tokenizer.key_word() == _xml_tag('keyword', 'else'))):

            self._write(self.tokenizer.key_word())

            self.tokenizer.advance()
            self._write(self.tokenizer.symbol())  # {

            self.tokenizer.advance()
            self.compile_statements()

            self._write(self.tokenizer.symbol())  # }

            self.tokenizer.advance()

    @_wrap_output_in_xml_tag('expression')
    def compile_expression(self):
        self.compile_term()

        if ((self.tokenizer.token_type() == 'symbol') and
            (self.tokenizer.symbol() in OP_SYMBOL_TOKENS)):

            self._write(self.tokenizer.symbol())

            self.tokenizer.advance()
            self.compile_term()


    @_wrap_output_in_xml_tag('term')
    def compile_term(self):
        if self.tokenizer.token_type() == 'INT_CONST':
            self._write(self.tokenizer.int_val())

        elif self.tokenizer.token_type() == 'STRING_CONST':
            self._write(self.tokenizer.string_val())

        elif ((self.tokenizer.token_type() == 'KEYWORD') and
              (self.tokenizer.key_word() in KEYWORD_CONSTANT_TOKENS)):
            self._write(self.tokenizer.key_word())

        elif self.tokenizer.token_type() == 'IDENTIFIER':
            self._write(self.tokenizer.identifier())

            #TODO: change this to _compile square_bracket variable
            self.tokenizer.advance()
            self._write(self.tokenizer.identifier())  # varName

            self.tokenizer.advance()
            if ((self.tokenizer.token_type() == 'symbol') and
                (self.tokenizer.symbol() == _xml_tag('['))):

                self._write(self.tokenizer.symbol())  # [

                self.tokenizer.advance()
                self.compile_expression()

                self.tokenizer.advance()
                self._write(self.tokenizer.symbol())  # ]

                self.tokenizer.advance()

        elif ((self.tokenizer.token_type() == 'symbol') and
              (self.tokenizer.symbol() == _xml_tag('('))):

            self._write(self.tokenizer.symbol())  # (

            self.tokenizer.advance()
            self.compile_expression()

            self._write(self.tokenizer.symbol())  # )

        elif ((self.tokenizer.token_type() == 'symbol') and
              (self.tokenizer.symbol() in UNARY_OP_KEYWORD_TOKENS)):

            self._write(self.tokenizer.symbol())  # "-" or "~"

            self.tokenizer.advance()
            self.compile_term()

        else:
            self._compile_subroutine_call()


    @_wrap_output_in_xml_tag('expressionList')
    def compile_expression_list(self):
        self.compile_expression()

        self.tokenizer.advance()
        while ((self.tokenizer.token_type() == 'symbol') and
               (self.tokenizer.symbol() == _xml_tag(','))):

            self.compile_expression()
            self.tokenizer.advance()
