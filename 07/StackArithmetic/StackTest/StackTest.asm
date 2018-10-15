
// // push constant x
@17
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@17
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // equals
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=D-M

@TEST_EQUAL$0
D;JEQ

D=0

@END_TEST$0
0;JMP

(TEST_EQUAL$0)
D=-1

(END_TEST$0)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@17
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@16
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // equals
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=D-M

@TEST_EQUAL$1
D;JEQ

D=0

@END_TEST$1
0;JMP

(TEST_EQUAL$1)
D=-1

(END_TEST$1)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@16
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@17
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // equals
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=D-M

@TEST_EQUAL$2
D;JEQ

D=0

@END_TEST$2
0;JMP

(TEST_EQUAL$2)
D=-1

(END_TEST$2)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@892
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@891
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

@TEST_LT$3
D;JLT

D=0

@END_TEST$3
0;JMP

(TEST_LT$3)
D=-1

(END_TEST$3)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@891
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@892
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

@TEST_LT$4
D;JLT

D=0

@END_TEST$4
0;JMP

(TEST_LT$4)
D=-1

(END_TEST$4)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@891
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@891
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

@TEST_LT$5
D;JLT

D=0

@END_TEST$5
0;JMP

(TEST_LT$5)
D=-1

(END_TEST$5)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@32767
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@32766
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // gt
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=M-D

@TEST_GT$6
D;JGT

D=0

@END_TEST$6
0;JMP

(TEST_GT$6)
D=-1

(END_TEST$6)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@32766
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@32767
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // gt
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=M-D

@TEST_GT$7
D;JGT

D=0

@END_TEST$7
0;JMP

(TEST_GT$7)
D=-1

(END_TEST$7)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@32766
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@32766
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // gt
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=M-D

@TEST_GT$8
D;JGT

D=0

@END_TEST$8
0;JMP

(TEST_GT$8)
D=-1

(END_TEST$8)

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@57
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@31
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1

// // push constant x
@53
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

// // push constant x
@112
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
// // negate
@SP // load value at top of stack
M=M-1
A=M

M=-M

@SP  // increment stack pointer
M=M+1


// // and
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=D&M

@SP // place result at top of stack
A=M
M=D

@SP  // increment stack pointer
M=M+1

// // push constant x
@82
D=A
@SP
A=M
M=D

@SP // increment stack pointer
M=M+1


// // or
@SP // load value at top of stack
M=M-1
A=M

D=M

@SP // load value at top of stack
M=M-1
A=M

D=D|M

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
