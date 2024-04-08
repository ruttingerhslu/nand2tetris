// Push constant10 to stack
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into localat index0
@SP
M = M - 1
A = M
D = M
@LCL
A = M
@0
A = A + D
M = D
// Push constant21 to stack
@21
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Push constant22 to stack
@22
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into argumentat index2
@SP
M = M - 1
A = M
D = M
@ARG
A = M
@2
A = A + D
M = D
// Pop stack into argumentat index1
@SP
M = M - 1
A = M
D = M
@ARG
A = M
@1
A = A + D
M = D
// Push constant36 to stack
@36
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into thisat index6
@SP
M = M - 1
A = M
D = M
@THIS
A = M
@6
A = A + D
M = D
// Push constant42 to stack
@42
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Push constant45 to stack
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into thatat index5
@SP
M = M - 1
A = M
D = M
@THAT
A = M
@5
A = A + D
M = D
// Pop stack into thatat index2
@SP
M = M - 1
A = M
D = M
@THAT
A = M
@2
A = A + D
M = D
// Push constant510 to stack
@510
D = A
@SP
A = M
M = D
@SP
M = M + 1
// Pop stack into tempat index6
@SP
M = M - 1
A = M
D = M
@TEMP
A = M
@6
A = A + D
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
