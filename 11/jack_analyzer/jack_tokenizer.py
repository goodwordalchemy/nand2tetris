import re
from lxml import etree

from .utils import get_output_filename, find_character_indices, split_text_preserving_quotes

COMMENT_PATTERNS = [
    r'/\*[\s\S]*? \*/\n', r'(//.*?)\n',
]
IDENTIFIER_PATTERN = '^[^\d\W]\w*\Z'
INT_CONST_PATTERN = r'^([0-9]\d{0,3}|[12]\d{4}|3[01]\d{3}|32[0-6]\d{2}|327[0-5]\d|3276[0-7])$'
STRING_CONST_PATTERN = r'^".*?"$'

SYMBOL_TOKENS = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
    '/', '&', '|', '<', '>', '=', '~',
]
KEYWORD_TOKENS = [
    'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
    'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
    'let', 'do', 'if', 'else', 'while', 'return',
]
EXCEPTION_FORMAT = 'this method should only be called if current token is a/an {}'

SYMBOL_REPLACEMENT_MAPPER = {'>': '&gt;', '<': '&lt;', '"': '&quot;', '&': '&amp;'}

def _remove_comments(content):
    for comment_pattern in COMMENT_PATTERNS:
        content = re.sub(comment_pattern, '\n', content)

    return content


def _pad_lexical_symbols(content):
    for st in SYMBOL_TOKENS:
        content = content.replace(st, ' {} '.format(st))

    return content


def get_token_list(content):
    content = _remove_comments(content)

    content = _pad_lexical_symbols(content)

    content = split_text_preserving_quotes(content)

    return content


class JackTokenizer:
    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            content = f.read()

        self.token_list = get_token_list(content)
        self.current_token = None

    def has_more_tokens(self):
        return len(self.token_list) > 0

    def advance(self):
        if not self.has_more_tokens():
            raise Exception('No more tokens to tokenize!')

        self.current_token = self.token_list.pop(0)

    def token_type(self):
        if self.current_token in KEYWORD_TOKENS:
            return 'KEYWORD'

        elif self.current_token in SYMBOL_TOKENS:
            return 'SYMBOL'

        elif re.match(IDENTIFIER_PATTERN, self.current_token):
            return 'IDENTIFIER'

        elif re.match(INT_CONST_PATTERN, self.current_token):
            return 'INT_CONST'

        elif re.match(STRING_CONST_PATTERN, self.current_token):
            return 'STRING_CONST'

        else:
            raise Exception('Unidentified token type: {}'.format(self.current_token))

    def key_word(self):
        if not self.token_type() == 'KEYWORD':
            raise Exception(EXCEPTION_FORMAT.format('KEYWORD'))

        return '<keyword> {} </keyword>\n'.format(self.current_token)

    def symbol(self):
        if not self.token_type() == 'SYMBOL':
            raise Exception(EXCEPTION_FORMAT.format('SYMBOL'))

        return '<symbol> {} </symbol>\n'.format(
            SYMBOL_REPLACEMENT_MAPPER.get(self.current_token, self.current_token)
        )

    def int_val(self):
        if not self.token_type() == 'INT_CONST':
            raise Exception(EXCEPTION_FORMAT.format('INT_CONST'))

        return '<integerConstant> {} </integerConstant>\n'.format(self.current_token)

    def identifier(self):
        if not self.token_type() == 'IDENTIFIER':
            raise Exception(EXCEPTION_FORMAT.format('IDENTIFIER'))

        return '<identifier> {} </identifier>\n'.format(self.current_token)

    def string_val(self):
        if not self.token_type() == 'STRING_CONST':
            raise Exception(EXCEPTION_FORMAT.format('STRING_CONST'))

        return '<stringConstant> {} </stringConstant>\n'.format(self.current_token[1:-1])


def tokenize_jack_file(input_file):
    tokenizer = JackTokenizer(input_file)

    output = ''

    while tokenizer.has_more_tokens():
        tokenizer.advance()

        token_type = tokenizer.token_type()

        if token_type == 'KEYWORD':
            output += tokenizer.key_word()

        elif token_type == 'SYMBOL':
            output += tokenizer.symbol()

        elif token_type == 'INT_CONST':
            output += tokenizer.int_val()

        elif token_type == 'STRING_CONST':
            output += tokenizer.string_val()

        elif token_type == 'IDENTIFIER':
            output += tokenizer.identifier()

    return output


def _wrap_output_in_token_tags(output):
    output = '<tokens>\n' + output + '</tokens>'

    return output


def main(input_file):
    output = tokenize_jack_file(input_file)
    output = _wrap_output_in_token_tags(output)

    output_filename = get_output_filename(input_file, output_file_ext='T.xml')
    print('tokenizer created file: {}'.format(output_filename))

    with open(output_filename, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    import sys

    main(sys.argv[1])
