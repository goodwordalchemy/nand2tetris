_POP_STACK1_TO_d_AND_POINT_a_REGISTER_AT_STACK2 = '''
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M
'''

_PUSH_D_TO_TOP_OF_STACK = '''
@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1
'''

def _wrap_binary_stack_operation(label, inner_asm_code):
    return (
        '\n\n// // ' + label +
        _POP_STACK1_TO_d_AND_POINT_a_REGISTER_AT_STACK2 +
        inner_asm_code +
        _PUSH_D_TO_TOP_OF_STACK
    )


ADD_COMMAND = _wrap_binary_stack_operation('add', '''
D=D+M
''')


SUBTRACT_COMMAND = _wrap_binary_stack_operation('subtract', '''
D=M-D
''')


NEGATE_COMMAND = '''// // negate
@SP // load value at top of stack
M=M-1
A=M

M=-M

@SP  // increment stack pointer
M=M+1
'''


# TODO: wrap comparisons
EQUALS_COMMAND = _wrap_binary_stack_operation('equals', '''
D=D-M

@TEST_EQUAL${unique_label}
D;JEQ

D=0

@END_TEST${unique_label}
0;JMP

(TEST_EQUAL${unique_label})
D=-1

(END_TEST${unique_label})
''')


GT_COMMAND = _wrap_binary_stack_operation('gt', '''
D=M-D

@TEST_GT${unique_label}
D;JGT

D=0

@END_TEST${unique_label}
0;JMP

(TEST_GT${unique_label})
D=-1

(END_TEST${unique_label})
''')


LT_COMMAND = _wrap_binary_stack_operation('lt', '''
D=M-D

@TEST_LT${unique_label}
D;JLT

D=0

@END_TEST${unique_label}
0;JMP

(TEST_LT${unique_label})
D=-1

(END_TEST${unique_label})
''')


AND_COMMAND = _wrap_binary_stack_operation('and', '''
D=D&M
''')


OR_COMMAND = _wrap_binary_stack_operation('or', '''
D=D|M
''')


NOT_COMMAND = '''// // not
@SP // load value at top of stack
M=M-1
A=M

M=!M

@SP  // increment stack pointer
M=M+1
'''
