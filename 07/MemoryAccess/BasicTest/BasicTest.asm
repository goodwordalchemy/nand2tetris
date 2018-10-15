// // push constant x
@10
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
// // push constant x
@21
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // push constant x
@22
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // pop argument x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store ARG + index in R14
@2
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
// // pop argument x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store ARG + index in R14
@1
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
// // push constant x
@36
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
@6
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
@42
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // push constant x
@45
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
@5
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
// // pop that x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D
// store THAT + index in R14
@2
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
// // push constant x
@510
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // pop temp x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store temp address in R14
@11
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
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
//// push that x
@5
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
// // push argument x
@1
D=A
@ARG
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
// // push this x
@6
D=A
@THIS
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push this x
@6
D=A
@THIS
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
// // push temp x
@11
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
