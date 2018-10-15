// // push constant x
@0
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // pop local x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store LCL + index in R14
@0
D=A
@LCL
D=D+M
@R14
M=D

@R13 // store value at R13 in RAM[LCL+index]
D=M
@R14
A=M
M=D
(LOOP_START)// // push argument x
@0
D=A
@ARG
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push local x
@0
D=A
@LCL
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
// // pop local x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store LCL + index in R14
@0
D=A
@LCL
D=D+M
@R14
M=D

@R13 // store value at R13 in RAM[LCL+index]
D=M
@R14
A=M
M=D
// // push argument x
@0
D=A
@ARG
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push constant x
@1
D=A

@SP
A=M
M=D

@SP // increment stack pointer
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
// // pop argument x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store ARG + index in R14
@0
D=A
@ARG
D=D+M
@R14
M=D

@R13 // store value at R13 in RAM[ARG+index]
D=M
@R14
A=M
M=D
// // push argument x
@0
D=A
@ARG
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
// // if-goto label
@SP // load value at top of stack
M=M-1
A=M

D=M

@LOOP_START
D;JNE
// // push local x
@0
D=A
@LCL
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
