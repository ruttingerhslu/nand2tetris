class CodeWriter:
    # 0 stands for unary, 1 stands for binary operation
    operations = {
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
        self._currFileName = ''
        self._currFunction = ''
        self._symbolTable = {}

    def _getCurrLine(self):
        line_count = 0
        for line in self._file:
            line = line.strip()
            if line and not line.startswith('//'):
                line_count += 1
        return line_count

    def _getBinaryOperation(self, operator):
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
            'M = M + 1\n' # increment SP to empty space

    def _getUnaryOperation(self, operator):
        return \
            '// Unary operation: ' + operator + '\n'+\
            '@SP\n'+\
            'M = M - 1\n'+\
            'A = M\n'+\
            'M = ' + operator + ' M\n'+\
            '@SP\n'+\
            'M = M + 1\n' # increment SP to empty space

    def _writePush(self, sgmt, id):
        sgmt_symbol = self._segments[sgmt]
        self._file.write(
            '// Push into stack from '+ sgmt +' at index: ' + id + ' \n'+
            '@'+ id +'\n'+
            'D = A\n'+
            '@'+ sgmt_symbol +'\n'+
            'A = M\n'+
            'A = A + D\n'+
            'D = M\n'+
            '@SP\n'+
            'A = M\n'+
            'M = D\n'+
            '@SP\n'+
            'M = M + 1\n' # increment SP to empty space
        )


    def _writePop(self, sgmt, id):
        sgmt_symbol = self._segments[sgmt]
        self._file.write(
            '// Pop stack into '+ sgmt + ' at index: ' + id + '\n'+
            '@' + sgmt_symbol + '\n'+
            'A = M\n'+
            'D = A\n'+
            '@'+ id +'\n'+
            'A = A+D\n'+
            'D = A\n'+
            '@R13\n'+
            'M = D\n'+
            '@SP\n'+
            'AM = M - 1\n'+
            'D = M\n'+
            '@R13\n'+
            'A = M\n'+
            'M = D\n'
        )


    def _writePushConstant(self, constant):
        self._file.write(
            '// Push constant ' + constant + ' to stack\n' +
            '@'+ constant +'\n'+
            'D = A\n' +
            '@SP\n' +
            'A = M\n' +
            'M = D\n' +
            '@SP\n' +
            'M = M + 1\n'
        )
    
    def _getPushSegment(self, sgmt_symbol):
        return \
            '// Push segment ' + sgmt_symbol + ' to stack\n'+\
            '@' + sgmt_symbol + '\n' +\
            'D = M\n' +\
            '@SP\n' +\
            'A=M\n' +\
            'M=D\n' +\
            '@SP\n' +\
            'M=M+1\n'

    def _getRestoreSegment(self, sgmt_symbol):
        return \
            '// Restore segment ' + sgmt_symbol + ' from caller (R13)\n'+\
            '@R13\n' +\
            'AM=M-1\n' +\
            'D=M\n' +\
            '@'+ sgmt_symbol +'\n' +\
            'M=D\n'

    def writeArithmetic(self, cmd):
        operator = self._operations[cmd][0]
        if not self._operations[cmd][1]:
            self._file.write(self._getUnaryOperation(operator))
        else:
            self._file.write(self._getBinaryOperation(operator))

    def writePushPop(self, cmd, sgmt, id):
        if cmd == 'C_PUSH':
            if sgmt == 'constant':
                self._writePushConstant(id)
            else:
                self._writePush(sgmt, id)
        elif cmd == 'C_POP':
            self._writePop(sgmt, id)

    def writeLabel(self, label):
        self._file.write(
            '// label: ' + label + '\n' +
            '(' + label + ')\n'
        )
        # SAVE NEW LABEL TO SYMBOL TABLE OF CURRENT FUNCTION
        self._symbolTable[self._currFunction][label] = self._getCurrLine()

    def writeGoto(self, label):
        # CHECK IF LABEL IS IN CURRENT FUNCTION
        if label in self._symbolTable[self._currFunction]:
            self._file.write(
                '// goto label: ' + label + '\n' +
                '@' + label + '\n' +
                '0; JMP\n'
            )
    
    def writeIf(self, label):
        # CHECK IF LABEL IS IN CURRENT FUNCTION
        if label in self._symbolTable[self._currFunction]:
            self._file.write(
                '// if-goto label: ' + label + '\n' +
                '@SP\n' +
                'M=M-1\n' +
                'A=M\n' +
                'D=M\n' +
                '@' + label + '\n' +
                'D;JNE\n'
            )

    def writeFunction(self, funcName, nVars):
        # SAVE CURRENT FUNCTION IN SYMBOL TABLE
        self._symbolTable.update(funcName)
        self._file.write(
            '// Allocate space for local variables\n' +
            '@' + num_locals + '\n' +
            'D=A\n' +
            '@SP\n' +
            'A=M\n' +
            'M=D\n' +
            '@SP\n' +
            'M=M+1\n' +
            '// Function '+ funcName +' with ' + nVars + ' variables \n'+
            '(' + function_name + ')\n'
        )
    
    def writeCall(self, funcName, nArgs):
        self._file.write(
            '// Call function\n' +
            # push return address
            self._getPushSegment('rAdd') +
            # push LCL
            self._getPushSegment('LCL') +
            # push ARG
            self._getPushSegment('ARG') +
            # push THIS
            self._getPushSegment('THIS') +
            # push THAT
            self._getPushSegment('THAT') +
            # set ARG for callee
            '@SP\n' +                                   
            'D=M\n' +
            '@5\n' +
            'D=D-A\n' +
            '@' + num_args + '\n' +
            'D=D-A\n' +
            '@ARG\n' +
            'M=D\n' +
            # set LCL for callee
            '@SP\n' +                                   
            'D=M\n' +
            '@LCL\n' +
            'M=D\n' +
            # JMP to function
            '@' + function_name + '\n' +                
            '0;JMP\n' +
            # define return address label
            '(RETURN_ADDRESS_' + call_index + ')\n'     
        )
    
    def writeReturn(self):
        self._file.write(
            '// Write return\n' +
            # store LCL to R13
            '@LCL\n' +
            'D=M\n' +
            '@R13\n' +
            'M=D\n' +
            # load return address to R14
            '@5\n' +
            'A=D-A\n' +
            'D=M\n' +
            '@R14\n' +
            'M=D\n' +
            # reposition return value of caller
            '@SP\n' +
            'A=M-1\n' +
            'D=M\n' +
            '@ARG\n' +
            'A=M\n' +
            'M=D\n' +
            # restore SP of ARG
            '@ARG\n' +
            'D=M+1\n' +
            '@SP\n' +
            'M=D\n' +
            # restore THAT of caller
            self._getRestoreSegment('THAT') +
            # restore THIS of caller
            self._getRestoreSegment('THIS') +
            # restore ARG of caller
            self._getRestoreSegment('ARG') +
            # restore LCL of caller
            self._getRestoreSegment('LCL') +
            # JMP to return address
            '@R14\n' +
            'A=M\n' +
            '0;JMP\n'
        )

    def appendInfinite(self):
        infiniteLoop = \
            '(END)\n' + \
            '@END\n' + \
            '0; JMP\n'
        self._file.write(infiniteLoop)
        self._file.close()