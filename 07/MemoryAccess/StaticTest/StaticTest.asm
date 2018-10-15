// // push constant x
@111
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // push constant x
@333
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // push constant x
@888
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@StaticTest.8
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@StaticTest.3
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@StaticTest.1
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // push static x
@StaticTest.3
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push static x
@StaticTest.1
D=M

@SP
A=M
M=D

@SP
M=M+1


// // subtract
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=M-D

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1
// // push static x
@StaticTest.8
D=M

@SP
A=M
M=D

@SP
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
