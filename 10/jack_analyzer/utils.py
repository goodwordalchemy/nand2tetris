import os

INPUT_FILE_EXT = '.jack'
OUTPUT_FILE_EXT = '.xml'

def get_output_filename(input_file, output_file_ext=OUTPUT_FILE_EXT):
    if os.path.isdir(input_file):
        filename = input_file.split('/')[-2]
        output_file = os.path.join(input_file, filename) + output_file_ext
    else:
        output_file =  os.path.splitext(input_file)[0] + output_file_ext

    return output_file

def get_input_files(input_path, input_file_ext=INPUT_FILE_EXT):
    if not os.path.isdir(input_path):
        return input_path

    paths = []
    for dirpath,_,filenames in os.walk(input_path):
        for f in filenames:
            if f.endswith(input_file_ext):
                paths.append(os.path.join(dirpath, f))
    return paths


def find_character_indices(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def split_text_preserving_quotes(content, include_quotes=False):
    quote_indices = find_character_indices(content, '"')

    if not quote_indices:
        return content.split()

    output = content[:quote_indices[0]].split()

    for i in range(1, len(quote_indices)):
        if i % 2 == 1: # end of quoted sequence
            start = quote_indices[i - 1]
            end = quote_indices[i] + 1
            string_section = content[start:end]
            output.extend([string_section])

        else:
            start = quote_indices[i - 1] + 1
            end = quote_indices[i]
            split_section = content[start:end].split()
            output.extend(split_section)

    output.extend(content[quote_indices[-1] + 1:].split())

    return output

if __name__ == '__main__':
    import sys

    with open(sys.argv[1], 'r') as f:
        data = f.read()

    print(split_text_preserving_quotes(data))
