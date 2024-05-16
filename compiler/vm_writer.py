from typing import Tuple, Literal

PushSegment = Tuple[Literal['CONSTANT'], Literal['ARGUMENT'], Literal['LOCAL'], Literal['STATIC'], Literal['THIS'], Literal['THAT'], Literal['POINTER'], Literal['TEMP']]
PopSegment = Tuple[Literal['ARGUMENT'], Literal['LOCAL'], Literal['STATIC'], Literal['THIS'], Literal['THAT'], Literal['POINTER'], Literal['TEMP']]
Command = Tuple[Literal['add'], Literal['sub'], Literal['neg'], Literal['eq'], Literal['gt'], Literal['lt'], Literal['and'], Literal['or'], Literal['not']]

class VMWriter:
    def __init__(self, vm_file):
        self._file = open(vm_file, 'w')
    
    def writePush(self, segment: PushSegment, index: int):
        self._file.write(f'push {segment} {index}\n')

    def writePop(self, segment: PopSegment, index: int):
        self._file.write(f'pop {segment} {index}\n')

    def writeArithmetic(self, command: Command):
        self._file.write(f'{command}\n')

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