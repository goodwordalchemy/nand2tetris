BOOTSTRAP_CODE = '''// Bootstrap code
@256
D=A
@SP
M=D
'''


GO_TO_COMMAND = '''// // goto label
@{label}
0;JMP
'''

IF_COMMAND = '''// // if-goto label
@SP // load value at top of stack
M=M-1
A=M

D=M

@{label}
D;JNE
'''
