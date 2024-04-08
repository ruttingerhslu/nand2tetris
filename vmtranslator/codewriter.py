from curses.ascii import SP

class CodeWriter:
    # 0 stands for unary, 1 stands for binary operation
    _operations = {
        'add': ['+', 1],
        'sub': ['-', 1],
        'neg': ['-', 0],
        'eq': ['==', 1],
        'gt': ['>', 1],
        'lt': ['<', 1],
        'and': ['&', 1],
        'or': ['|', 1],
        'not': ['!', 0]
    }

    _segments = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'temp': 'TEMP',
    } 

    def __init__(self, asm_file):
        self._file = open(asm_file, 'w')

    def _binaryOperation(self, operator):
        return \
            '// Binary operation: ' + operator + '\n'+\
            '@SP\n'+\
            'M = M - 1\n'+\
            'A = M\n'+\
            'D = M\n'+\
            '@SP\n'+\
            'M = M - 1\n'+\
            'A = M\n'+\
            'M = M ' + operator + ' D\n'+\
            '@SP\n'+\
            'M = M + 1' # increment SP to empty space
    
    def _unaryOperation(self, operator):
        return \
            '// Unary operation: ' + operator + '\n'+\
            '@SP\n'+\
            'M = M - 1\n'+\
            'A = M\n'+\
            'M = ' + operator + ' M\n'+\
            '@SP\n'+\
            'M = M + 1' # increment SP to empty space
        
    def writeArithmetic(self, cmd):
        operator = self._operations[cmd][0]
        if not self._operations[cmd][1]:
            self._unaryOperation(operator)
        else:
            self._binaryOperation(operator)

    def _writePush(self, sgmt, id):
        sgmt_symbol = self._segments[sgmt]
        return \
            '// Push into stack from '+ sgmt +' at index: ' + id + ' \n'+\
            '@'+ id +'\n'+\
            'D = A\n'+\
            '@'+ sgmt_symbol +'\n'+\
            'A = M\n'+\
            'A = A + D\n'+\
            'D = M\n'+\
            '@SP\n'+\
            'A = M\n'+\
            'M = D\n'+\
            '@SP\n'+\
            'M = M + 1' # increment SP to empty space
    
    def _writePop(self, sgmt, id):
        sgmt_symbol = self._segments[sgmt]
        return \
            '// Pop stack into '+ sgmt + 'at index' + id + '\n'+\
            '@SP\n'+\
            'M = M - 1\n'+\
            'A = M\n'+\
            'D = M\n'+\
            '@' + sgmt_symbol + '\n'+\
            'A = M\n'+\
            '@' + id + '\n'+\
            'A = A + D\n'+\
            'M = D'

    
    def writePushPop(self, cmd, sgmt, id):
        if cmd == 'C_PUSH':
            if (sgmt == 'static'):
                self._writePush(self, )
            else:
            self._writePush(self, sgmt, id)
        elif cmd == 'C_POP':
            self._writePop(self, sgmt, id)