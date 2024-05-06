type PushSegment = tuple('CONSTANT', 'ARGUMENT', 'LOCAL', 'STATIC', 'THIS', 'THAT', 'POINTER', 'TEMP')
type PopSegment = tuple('ARGUMENT', 'LOCAL', 'STATIC', 'THIS', 'THAT', 'POINTER', 'TEMP')
type Command = tuple('ADD', 'SUB', 'NEG', 'EQ', 'GT', 'LT', 'AND', 'OR', 'NOT')

class VMWriter:
    def __init__(self, vm_file):
        self._file = open(vm_file, 'w')

    def writePush(self, segment: PushSegment, index: int):
        self._file.write('PUSH COMMAND')
    
    def writePop(self, segment: PopSegment, index: int):
        self._file.write('POP COMMAND')

    def writeArithmetic(self, command: Command):
        self._file.write('ARITHMETIC COMMAND')
    
    def writeLabel(self, label: str):
        self._file.write('(' + label + ')')

    def writeGoto(self, label: str):
        self._file.write('GOTO')
    
    def writeIf(self, label: str):
        self._file.write('IF CMD')
    
    def writeCall(self, name: str, nArgs: int):
        self._file.write('CALL COMMAND')
    
    def writeFunction(self, name: str, nVars: int):
        self._file.write('FUNCTION COMMAND')

    def writeReturn(self):
        self._file.write('RETURN COMMAND')
    
    def close(self):
        self._file.close()