import sys
from parser import Parser
from codewriter import CodeWriter

class VMTranslator:
    def __init__(self, file):
        self._translate(file)

    def _to_asm_file(self,  vm_file):
        return vm_file.replace('.vm', '.asm')

    def _translate(self, file):
        parser = Parser(file)
        codeWriter = CodeWriter(self._to_asm_file(file))
        while parser.hasMoreLines():
            parser.advance()
            cmdType = parser.commandType()
            if cmdType != 'C_RETURN':
                arg1 = parser.arg1()
                if cmdType in {'C_PUSH','C_POP', 'C_FUNCTION', 'C_CALL'}:
                    arg2 = parser.arg2()
                    codeWriter.writePushPop(cmdType, arg1, arg2)
                else:
                    codeWriter.writeArithmetic(arg1)
        codeWriter.appendInfinite()

if __name__ == '__main__':
    vm_file = sys.argv[1]
    VMTranslator(vm_file)