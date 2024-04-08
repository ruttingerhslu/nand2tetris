    @i // i bezieht sich auf einen Speicherplatz.
    M = 1 // i = 1
    @sum // sum bezieht sich auf einen Speicherplatz.
    M = 0 // sum = 0
(LOOP)
    @i
    D = M
    @R0
    D = D - M
    @END
    D; JGT // Wenn (i - R0) > 0 goto END
    @R1
    D = M
    @sum
    M = D + M // sum = sum + R1
    @i
    M = M + 1 // i = i + 1
    @LOOP
    0; JMP // Springe zu LOOP
(END)
    @sum
    D = M
    @R2
    M = D
    @END
    0; JMP // Endlosschleife