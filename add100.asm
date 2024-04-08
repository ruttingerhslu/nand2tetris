// Addiert 1 + ... + 100.
    @i // i bezieht sich auf einen Speicherplatz.
    M = 1 // i = 1
    @sum // sum bezieht sich auf einen Speicherplatz.
    M = 0 // sum = 0
(LOOP)
    @i
    D = M // D = i
    @100
    D = D - A // D = i - 100
    @END
    D; JGT // Wenn (i - 100) > 0 goto END
    @i
    D = M // D = i
    @sum
    M = D + M // sum = sum + i
    @i
    M = M + 1 // i = i + 1
    @LOOP
    0; JMP // Springe zu LOOP
(END)
    @END
    0; JMP // Endlosschleife