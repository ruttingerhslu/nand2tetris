from lex import Lex, NUMBER, SYMBOL, OPERATION

class Parser:
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2

    def __init__(self, file):
        self.lexer = Lex(file)
        self._init_instruction_info()

    def _init_instruction_info(self):
        self._instructionType = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''

    def _a_instruction(self):
        self._instructionType = Parser.A_INSTRUCTION
        tok_type, self._symbol = self.lexer.next_token()

    def _l_instruction(self):
        self._instructionType = Parser.L_INSTRUCTION
        tok_type, self._symbol = self.lexer.next_token()

    def _c_instruction(self, token, value):
        self._instructionType = Parser.C_INSTRUCTION
        comp_tok, comp_val = self._get_dest(token, value)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    def _get_dest(self, token, value):
        tok2, val2 = self.lexer.peek_token()
        if tok2 == OPERATION and val2 == '=':
            self.lexer.next_token()
            self._dest = value
            comp_tok, comp_val = self.lexer.next_token()
        else:
            comp_tok, comp_val = token, value
        return comp_tok, comp_val

    def _get_comp(self, token, value):
        if token == OPERATION and (value == '-' or value == '!'):
            tok2, val2 = self.lexer.next_token()
            self._comp = value + val2
        elif token == NUMBER or token == SYMBOL:
            self._comp = value
            tok2, val2 = self.lexer.peek_token()
            if tok2 == OPERATION and val2 != ';':
                self.lexer.next_token()
                tok3, val3 = self.lexer.next_token()
                self._comp += val2+val3

    def _get_jump(self):
        token, value = self.lexer.next_token()
        if token == OPERATION and value == ';':
            jump_tok, jump_val = self.lexer.next_token()
            self._jmp = jump_val

    @property
    def instructionType(self):
        return self._instructionType

    @property
    def symbol(self):
        return self._symbol

    @property
    def dest(self):
        return self._dest

    @property
    def comp(self):
        return self._comp

    @property
    def jmp(self):
        return self._jmp

    def hasMoreLines(self):
        return self.lexer.has_more_instructions()

    def advance(self):
        self._init_instruction_info()

        self.lexer.next_instruction()
        token, val = self.lexer.curr_token

        if token == OPERATION and val == '@':
            self._a_instruction()
        elif token == OPERATION and val == '(':
            self._l_instruction()
        else:
            self._c_instruction(token, val)
