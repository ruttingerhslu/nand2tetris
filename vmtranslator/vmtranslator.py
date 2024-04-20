import sys
from parser import Parser
from codewriter import CodeWriter
import os

class VMTranslator:
    def __init__(self, path):
        if os.path.isdir(path):
            vm_files = [file for file in os.listdir(path) if file.endswith('.vm')]
            if vm_files:
                for vm_file in vm_files:
                    self._translate(vm_file)
            else:
                print(f"No files ending with .vm found in {path}.")
        elif os.path.isfile(path):
            if path.endswith('.vm'):
                self._translate(path)
            else:
                print(f"{path} is not the correct file format (.vm)")
        else:
            print(f"No file {path} found")

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
                match arg1:
                    case codeWriter.operations.keys():
                        codeWriter.writeArithmetic(arg1)
                    case ['C_PUSH','C_POP']:
                        arg2 = parser.arg2()
                        codeWriter.writePushPop(cmdType, arg1, arg2)
                    case 'C_LABEL':
                        codeWriter.writeLabel(arg1)
                    case 'C_GOTO':
                        codeWriter.writeGoto(arg1)
                    case 'C_IF':
                        codwWriter.writeIf(arg1)
        codeWriter.appendInfinite()

if __name__ == '__main__':
    vm_file = sys.argv[1]
    VMTranslator(vm_file)