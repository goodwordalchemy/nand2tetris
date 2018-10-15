// Bootstrap code
@256
D=A
@SP
M=D
// // call f n
// push return-address
@Sys.init$$$return-address0
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

@0
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
@Sys.init
0;JMP

// leave (return-address)
(Sys.init$$$return-address0)

//////// function declaration ////////
(Class1.set)// // push argument x
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
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@Class1.0
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
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
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@Class1.1
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // push constant x
@0
D=A

@SP
A=M
M=D

@SP // increment stack pointer
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

//////// end function declaration ////

//////// function declaration ////////
(Class1.get)// // push static x
@Class1.0
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push static x
@Class1.1
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

//////// end function declaration ////

//////// function declaration ////////
(Sys.init)// // push constant x
@6
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
// // call f n
// push return-address
@Class1.set$$$return-address1
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

@2
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
@Class1.set
0;JMP

// leave (return-address)
(Class1.set$$$return-address1)
// // pop temp x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store temp address in R14
@5
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // push constant x
@23
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // push constant x
@15
D=A

@SP
A=M
M=D

@SP // increment stack pointer
M=M+1
// // call f n
// push return-address
@Class2.set$$$return-address2
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

@2
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
@Class2.set
0;JMP

// leave (return-address)
(Class2.set$$$return-address2)
// // pop temp x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store temp address in R14
@5
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // call f n
// push return-address
@Class1.get$$$return-address3
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

@0
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
@Class1.get
0;JMP

// leave (return-address)
(Class1.get$$$return-address3)
// // call f n
// push return-address
@Class2.get$$$return-address4
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

@0
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
@Class2.get
0;JMP

// leave (return-address)
(Class2.get$$$return-address4)
(Sys.init$WHILE)
// // goto label
@Sys.init$WHILE
0;JMP

//////// function declaration ////////
(Class2.set)// // push argument x
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
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@Class2.0
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
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
// // pop static x
@SP // Pop top value off of stack and store in R13
M=M-1
A=M
D=M
@R13
M=D

// store static address in R14
@Class2.1
D=A
@R14
M=D

@R13 // store value at R13 in RAM[index]
D=M
@R14
A=M
M=D
// // push constant x
@0
D=A

@SP
A=M
M=D

@SP // increment stack pointer
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

//////// end function declaration ////

//////// function declaration ////////
(Class2.get)// // push static x
@Class2.0
D=M

@SP
A=M
M=D

@SP
M=M+1
// // push static x
@Class2.1
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

//////// end function declaration ////
