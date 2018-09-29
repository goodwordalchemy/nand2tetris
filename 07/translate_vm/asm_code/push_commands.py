PUSH_CONSTANT_COMMAND = '''// // push constant x
@{index}
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
'''


PUSH_LOCAL_COMMAND = '''// // push local x
@{index}
D=A
@LCL
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
'''


PUSH_ARGUMENT_COMMMAND = '''// // push argument x
@{index}
D=A
@ARG
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
'''


PUSH_THIS_COMMAND = '''// // push this x
@{index}
D=A
@THIS
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
'''

PUSH_THAT_COMMMAND = '''//// push that x
@{index}
D=A
@THAT
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
'''

PUSH_TEMP_COMMAND = '''// // push temp x
@{index}
D=M

@SP
A=M
M=D

@SP
M=M+1
'''


PUSH_POINTER_COMMAND = '''// // push pointer x
@{index}
D=A
@THIS
A=D+A
D=M

@SP
A=M
M=D

@SP
M=M+1
'''


PUSH_STATIC_COMMAND = '''// // push static x
@{filename}.{index}
D=M

@SP
A=M
M=D

@SP
M=M+1
'''
