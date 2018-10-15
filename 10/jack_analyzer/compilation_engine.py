def _xml_tag(tagname, inner):
    return '<{tagname}> {inner} </{tagname}>\n'.format(
        tagname=tagname, inner=inner
    )

CLASS_VAR_DEC_KEYWORD_TOKENS = [_xml_tag('keyword', kw) for kw in ['static', 'field']]
SUBROUTINE_DEC_KEYWORD_TOKENS = [_xml_tag('keyword', kw) for kw in ['constructor', 'function', 'method']]

class CompilationEngine:
    def __init__(self, tokenizer, output_filename):
        self.tokenizer = tokenizer
        self.tokenizer.advance()
        self.output_handle = open(output_filename, 'w')

    def _write(self, content):
        self.output_handle.write(content)

    def compile_class(self):
        self._write('<class>\n')

        # Tokenzizer is already advanced, like in other methods.
        self._write(self.tokenizer.key_word()) # "class"

        self.tokenizer.advance()
        self._write(self.tokenizer.identifier()) # className

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol()) # {

        self.tokenizer.advance()
        while ((self.tokenizer.token_type() == 'KEYWORD') and
               (self.tokenizer.key_word() in CLASS_VAR_DEC_KEYWORD_TOKENS)):
            self.compile_class_var_dec()
            self.tokenizer.advance()

        print(self.tokenizer.current_token)
        while ((self.tokenizer.token_type() == 'KEYWORD') and
               (self.tokenizer.key_word() in SUBROUTINE_DEC_KEYWORD_TOKENS)):
            self.compile_subroutine()
            self.tokenizer.advance()

        self._write(self.tokenizer.symbol()) # }

        self._write('<\class>\n')

    def compile_class_var_dec(self):
        self._write('<classVarDec>\n')

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

        self._write('</classVarDec>\n')

    def compile_subroutine(self):
        self._write('<subroutineDec>\n')

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

        self.tokenizer.advance()
        self._write(self.tokenizer.symbol()) # "}"

        self._write('</subroutineDec>\n')

    def compile_parameter_list(self):
        self._write('<parameterList>\n')

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

        self._write('</parameterList>\n')

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compiile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

