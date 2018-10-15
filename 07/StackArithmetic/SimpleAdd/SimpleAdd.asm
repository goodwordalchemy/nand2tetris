// // push constant x
@7
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // push constant x
@8
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // add
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=D+M

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1
