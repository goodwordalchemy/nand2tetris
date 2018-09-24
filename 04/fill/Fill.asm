// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
    // @16640 // 16384 + 256
    @24576
    D=A
    @endIdx
    M=D
(LOOP)
// Handle Keypress logic
    @KBD
    D=M
    @KEYPRESSED
    D;JGT
    @NOKEYPRESSED
    D;JEQ
(KEYPRESSED)
    @write
    M=-1
    @DRAWSCREEN
    0;JMP
(NOKEYPRESSED)
    @write
    M=0
    @DRAWSCREEN
    0;JMP
(DRAWSCREEN)
// Initialize screen looping variables
    @SCREEN
    D=A
    @row
    M=D
(DRAWSCREENLOOP)
    // write bit at register r
    @write
    D=M
    @row
    A=M
    M=D
    @row
    MD=M+1
    @endIdx
    D=D-M
    @DRAWSCREENLOOP
    D;JLT
@LOOP
0;JMP
   
    
    
