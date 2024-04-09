// Push constant 10 to stack
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into local at index: 0
@LCL
A = M
D = A
@0
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Push constant 21 to stack
@21
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Push constant 22 to stack
@22
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into argument at index: 2
@ARG
A = M
D = A
@2
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Pop stack into argument at index: 1
@ARG
A = M
D = A
@1
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Push constant 36 to stack
@36
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into this at index: 6
@THIS
A = M
D = A
@6
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Push constant 42 to stack
@42
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Push constant 45 to stack
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into that at index: 5
@THAT
A = M
D = A
@5
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Pop stack into that at index: 2
@THAT
A = M
D = A
@2
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Push constant 510 to stack
@510
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into temp at index: 6
@TEMP
A = M
D = A
@6
A = A+D
D = A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// Push into stack from local at index: 0 
@0
D = A
@LCL
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// Push into stack from that at index: 5 
@5
D = A
@THAT
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// Binary operation: +
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M + D
@SP
M = M + 1
// Push into stack from argument at index: 1 
@1
D = A
@ARG
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// Binary operation: -
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M - D
@SP
M = M + 1
// Push into stack from this at index: 6 
@6
D = A
@THIS
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// Push into stack from this at index: 6 
@6
D = A
@THIS
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// Binary operation: +
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M + D
@SP
M = M + 1
// Binary operation: -
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M - D
@SP
M = M + 1
// Push into stack from temp at index: 6 
@6
D = A
@TEMP
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// Binary operation: +
@SP
M = M - 1
A = M
D = M
@SP
M = M - 1
A = M
M = M + D
@SP
M = M + 1
(END)
@END
0; JMP
