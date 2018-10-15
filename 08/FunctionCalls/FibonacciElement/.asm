// Bootstrap code
@SP
M=256
// // call f n
// push return-address
@Sys.init==return-adress
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push LCL
@LCL
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push ARG
@ARG
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THIS
@THIS
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THAT
@THAT
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// ARG = SP-n-5
@SP
D=A

@0
D=D-A

@5
D=D-A

@ARG
M=D


// LCL = SP
@SP
D=A

@LCL
M=D

// goto f
@Sys.init
0;JMP

// leave (return-address)
(Sys.init==return-address)
//////// function declaration ////////(Main.fibonacci)//////// end function declaration ////
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
@2
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // lt
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=M-D

@TEST_LT$0
D;JLT

D=0

@END_TEST$0
0;JMP

(TEST_LT$0)
D=-1

(END_TEST$0)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1
// // if-goto label
@SP // load value at top of stack
M=M-1
A=M

D=M

@Sys.init$IF_TRUE
D;JNE
// // goto label
@Sys.init$IF_FALSE
0;JMP
(IF_TRUE)// // push argument x
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
(IF_FALSE)// // push argument x
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
@2
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
// // call f n
// push return-address
@Main.fibonacci==return-adress
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push LCL
@LCL
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push ARG
@ARG
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THIS
@THIS
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THAT
@THAT
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// ARG = SP-n-5
@SP
D=A

@1
D=D-A

@5
D=D-A

@ARG
M=D


// LCL = SP
@SP
D=A

@LCL
M=D

// goto f
@Main.fibonacci
0;JMP

// leave (return-address)
(Main.fibonacci==return-address)
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
// // call f n
// push return-address
@Main.fibonacci==return-adress
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push LCL
@LCL
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push ARG
@ARG
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THIS
@THIS
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THAT
@THAT
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// ARG = SP-n-5
@SP
D=A

@1
D=D-A

@5
D=D-A

@ARG
M=D


// LCL = SP
@SP
D=A

@LCL
M=D

// goto f
@Main.fibonacci
0;JMP

// leave (return-address)
(Main.fibonacci==return-address)


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
//////// function declaration ////////(Sys.init)//////// end function declaration ////
// // push constant x
@4
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // call f n
// push return-address
@Main.fibonacci==return-adress
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push LCL
@LCL
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push ARG
@ARG
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THIS
@THIS
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// push THAT
@THAT
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// ARG = SP-n-5
@SP
D=A

@1
D=D-A

@5
D=D-A

@ARG
M=D


// LCL = SP
@SP
D=A

@LCL
M=D

// goto f
@Main.fibonacci
0;JMP

// leave (return-address)
(Main.fibonacci==return-address)
(WHILE)// // goto label
@Main.fibonacci$WHILE
0;JMP
