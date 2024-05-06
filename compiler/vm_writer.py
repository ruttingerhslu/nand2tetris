type PushSegment = tuple('CONSTANT', 'ARGUMENT', 'LOCAL', 'STATIC', 'THIS', 'THAT', 'POINTER', 'TEMP')
type PopSegment = tuple('ARGUMENT', 'LOCAL', 'STATIC', 'THIS', 'THAT', 'POINTER', 'TEMP')
type Command = tuple('ADD', 'SUB', 'NEG', 'EQ', 'GT', 'LT', 'AND', 'OR', 'NOT')

class VMWriter:
    def __init__(self, vm_file):
        self._file = open(vm_file, 'w')
    
    def writePush(self, segment: PushSegment, index: int):
        self._file.write(f'push {segment.lower()} {index}\n')

    def writePop(self, segment: PopSegment, index: int):
        self._file.write(f'push {segment.lower()} {index}\n')

    def writeArithmetic(self, command: Command):
        self._file.write(f'{command.lower()}\n')

    def writeLabel(self, label: str):
        self._file.write(f'label {label}\n')

    def writeGoto(self, label: str):
        self._file.write(f'goto {label}\n')

    def writeIf(self, label: str):
        self._file.write(f'if-goto {label}\n')

    def writeCall(self, name: str, nArgs: int):
        self._file.write(f'call {name} {nArgs}\n')

    def writeFunction(self, name: str, nVars: int):
        self._file.write(f'function {name} {nVars}\n')

    def writeReturn(self):
        self._file.write('return\n')
    
    def close(self):
        self._file.close()