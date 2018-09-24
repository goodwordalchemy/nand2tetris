import sys

from .assemble import assemble

def main():
    input_file = sys.argv[1]

    assemble(input_file)

if __name__ == '__main__':
    main()
