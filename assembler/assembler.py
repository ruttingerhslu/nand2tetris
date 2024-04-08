import sys
from code import Code
from parser import Parser
from symbol_table import SymbolTable

class Assembler:
    def __init__(self):
        self.symbol_address = 16
        self.symbols_table = SymbolTable()

    @staticmethod
    def get_hack_file(asm_file):
        if asm_file.endswith('.asm'):
            return asm_file.replace('.asm', '.hack')
        else:
            return asm_file + '.hack'

    def _getAddress(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols_table.contains(symbol):
                self.symbols_table.addEntry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbols_table.getAddress(symbol)

    def pass_1(self, file):
        parser = Parser(file)
        curr_address = 0
        while parser.hasMoreLines():
            parser.advance()
            inst_type = parser.instructionType
            if inst_type in [parser.A_INSTRUCTION, parser.C_INSTRUCTION]:
                curr_address += 1
            elif inst_type == parser.L_INSTRUCTION:
                self.symbols_table.addEntry(parser.symbol, curr_address)

    def pass_2(self, asm_file, hack_file):
        parser = Parser(asm_file)
        with open(hack_file, 'w', encoding='utf-8') as hack_file:
            code = Code()
            while parser.hasMoreLines():
                parser.advance()
                inst_type = parser.instructionType
                if inst_type == parser.A_INSTRUCTION:
                    hack_file.write(code.gen_a_instruction(self._getAddress(parser.symbol)) + '\n')
                elif inst_type == parser.C_INSTRUCTION:
                    hack_file.write(code.gen_c_instruction(parser.dest, parser.comp, parser.jmp) + '\n')
                elif inst_type == parser.L_INSTRUCTION:
                    pass

    def assemble(self, file):
        self.pass_1(file)
        self.pass_2(file, self.get_hack_file(file))


if __name__ == '__main__':
    asm_file = sys.argv[1]

    hack_assembler = Assembler()
    hack_assembler.assemble(asm_file)