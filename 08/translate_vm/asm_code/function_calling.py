CALL_COMMAND = '''// // call f n
// push return-address
@{label}$$$return-address{unique_index}
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push LCL
@LCL
D=M

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push ARG
@ARG
D=M

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THIS
@THIS
D=M

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THAT
@THAT
D=M

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// ARG = SP-n-5
@SP
D=M

@{n_args}
D=D-A

@5
D=D-A

@ARG
M=D


// LCL = SP
@SP
D=M

@LCL
M=D

// goto f
@{label}
0;JMP

// leave (return-address)
({label}$$$return-address{unique_index})
'''


RETURN_COMMAND = '''// // return
// FRAME = LCL
@LCL
D=M
@R13
M=D

// RETURN = *(FRAME - 5)
@5
D=A
@R13
A=M-D
D=M
@R14
M=D

// *ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D

// SP = ARG+1
@ARG
D=M
@SP
M=D+1

// THAT = *(FRAME-1)
@R13
D=M
A=D-1
D=M
@THAT
M=D

// THIS = *(FRAME-2)
@R13
D=M
A=D-1
A=A-1
D=M
@THIS
M=D

// ARG = *(FRAME-3)
@R13
D=M
A=D-1
A=A-1
A=A-1
D=M
@ARG
M=D

// LCL = *(FRAME-4)
@R13
D=M
A=D-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D

// goto RET
@R14
A=M
0;JMP
'''
