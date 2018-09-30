_POP_TO_R13 = '''
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
'''

_VIRTUAL_COMMAND_FORMAT = '''// store {asm_keyword} + index in R14
@{{index}}
D=A
@{asm_keyword}
D=D+M
@R14
M=D

@R13 // store value at R13 in RAM[{asm_keyword}+index]
D=M
@R14
A=M
M=D
'''

def _get_pop_to_virtual_segment(label, asm_keyword):
    result_format_str = (
        '// // pop {label} x' +
        _POP_TO_R13 +
        _VIRTUAL_COMMAND_FORMAT
    )

    return result_format_str.format(label=label, asm_keyword=asm_keyword)


POP_LOCAL_COMMAND = _get_pop_to_virtual_segment('local', 'LCL')

POP_ARGUMENT_COMMAND = _get_pop_to_virtual_segment('argument', 'ARG')

POP_THIS_COMMAND = _get_pop_to_virtual_segment('this', 'THIS')

POP_THAT_COMMAND = _get_pop_to_virtual_segment('that', 'THAT')

POP_TEMP_COMMAND = (
    '// // pop temp x' +
    _POP_TO_R13 +
'''
// store temp address in R14
@{index}
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
'''
)


POP_POINTER_COMMAND = (
    ' // pop pointer x' +
    _POP_TO_R13 +
'''
@{index}
D=A
@THIS
D=D+A
@R14
M=D

@R13 // store value at R13 in RAM[this+index]
D=M
@R14
A=M
M=D
'''
)


POP_STATIC_COMMAND = (
    '// // pop static x' +
    _POP_TO_R13 +
'''
// store static address in R14
@{filename}.{index}
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
'''
)
