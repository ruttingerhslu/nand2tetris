import sys
from parser import Parser
from codewriter import CodeWriter

class VMTranslator:
    def __init__(self, file):
        self._pass_1(file)

    def _to_asm_file(self,  vm_file):
        return vm_file.replace('.vm', '.asm')

    def _translate(self, file):
        parser = Parser(file)
        codeWriter = CodeWriter(self._to_asm_file(file))
        while parser.hasMoreLines():
            parser.advance(file)
            cmdType = parser.commandType()
            if cmdType != 'C_RETURN':

                

    def _pass_2(self, vm_file, asm_file):
        parser = Parser(vm_file)
        code_writer = CodeWriter(asm_file)

        # -> append infinity loop
        # (END)
        # @END
        # 0; JMP

if __name__ == '__main__':
    vm_file = sys.argv[1]
    VMTranslator(vm_file)