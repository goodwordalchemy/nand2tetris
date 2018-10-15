// // push constant x
@3030
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
 // pop pointer x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

@0
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
// // push constant x
@3040
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
 // pop pointer x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

@1
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
// // push constant x
@32
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // pop this x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store THIS + index in R14
@2
D=A
@THIS
D=D+M
@R14
M=D

@R13 // store value at R13 in RAM[THIS+index]
D=M
@R14
A=M
M=D
// // push constant x
@46
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // pop that x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store THAT + index in R14
@6
D=A
@THAT
D=D+M
@R14
M=D

@R13 // store value at R13 in RAM[THAT+index]
D=M
@R14
A=M
M=D
// // push pointer x
@0
D=A
@THIS
A=D+A
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push pointer x
@1
D=A
@THIS
A=D+A
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
// // push this x
@2
D=A
@THIS
A=D+M
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
//// push that x
@6
D=A
@THAT
A=D+M
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
