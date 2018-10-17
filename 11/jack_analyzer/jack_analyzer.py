from .jack_tokenizer import JackTokenizer
from .compilation_engine import CompilationEngine
from .utils import get_input_files, get_output_filename


def analyze_jack(filename):
    tokenizer = JackTokenizer(filename)

    output_filename = get_output_filename(filename, '.xml')

    compilation_engine = CompilationEngine(tokenizer, output_filename)
    compilation_engine.compile_class()


def main(jack_file_or_directory):
    input_files = get_input_files(jack_file_or_directory)

    if not isinstance(input_files, list):
        input_files = [input_files]


    for f in input_files:
        analyze_jack(f)
