//////// function declaration ////////
(SimpleFunction.test)// // push local x
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
// // push local x
@1
D=A
@LCL
A=D+M
D=M

@SP
A=M
M=D

@SP
M=M+1
//////// end function declaration ////
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
// // push local x
@1
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
// // not
@SP // load value at top of stack
M=M-1
A=M

M=!M

@SP  // increment stack pointer
M=M+1
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
// // return
// FRAME = LCL
@LCL
D=M
@R13
M=D

// RETURN = *(FRAME - 5)
@5
D=A
@R13
D=M-D
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
