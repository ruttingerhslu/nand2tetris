from collections import deque

from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable
from vm_writer import VMWriter

class CompilationEngine:
    _binary_ops = {
        '+': 'add',
        '-': 'sub',
        '&': 'and',
        '|': 'or',
        '<': 'lt',
        '>': 'gt',
        '=': 'eq'
    }

    _unary_ops = {
        '-': 'neg',
        '~': 'not'
    }

    def __init__(self, read_file, write_file):
        self._read_file = read_file
        self._write_file = open(write_file, 'w')

        vm_file = read_file[:read_file.rfind('.jack')] + '.vm'
        self.vm_writer = VMWriter('./output/' + vm_file)

        self.tokenizer = JackTokenizer(read_file)
        self._curr_token = self.tokenizer.advance()

        self._tab_count = 0
        self._symbol_tables = deque()
        self._class_table = SymbolTable()
        self._method_table = SymbolTable()
        self._last_token = ''
        
        self._method_class = ''
        self._curr_class = ''

        self.compileClass()

    def printXMLToken(self, token):
        self._write_file.write(self.get_indent() + '<' + self.tokenizer.tokenType().lower() + '> ' +\
            token +\
            ' </' + self.tokenizer.tokenType().lower() + '>\n')
    
    def get_indent(self):
        return "\t" * self._tab_count

    def printXMLTag(self, tag):
        self._write_file.write(self.get_indent() + tag + '\n')

    def process(self, tokens):
        if self.tokenizer.hasMoreTokens():
            if isinstance(tokens, list):
                if (self._curr_token in tokens):
                    self.printXMLToken(self._curr_token)
                else:
                    print('syntax error')
            else:
                if (self._curr_token == tokens):
                    self.printXMLToken(self._curr_token)
                else:
                    print('syntax error')
            self._curr_token = self.tokenizer.advance()
        else:
            print('finished program')
    
    def get_types(self):
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            return [self.tokenizer.identifier()]
        elif self.tokenizer.tokenType() == 'KEYWORD':
            return ['int', 'char', 'boolean']
        else:
            return []
    
    def compileClass(self):
        self.printXMLTag('<class>')
        self._tab_count += 1
        self.process('class')
        self._curr_class = self.tokenizer.identifier()
        self.process(self.tokenizer.identifier())
        self.process('{')
        while self.tokenizer.keyWord() in ['static', 'field']:
            self.compileClassVarDec()
        while self.tokenizer.keyWord() in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
            self._method_table.reset()
        self.process('}')
        self._tab_count -= 1
        self.printXMLTag('</class>')
        self._class_table.reset()

    def compileClassVarDec(self):
        self.printXMLTag('<classVarDec>')
        self._tab_count += 1
        keyword = self.tokenizer.keyWord()
        self.process(['static', 'field'])
        idType = self.tokenizer.keyWord() or self.tokenizer.identifier()
        self.process(self.get_types())
        idName = self.tokenizer.identifier()
        self.process(self.tokenizer.identifier())
        self._class_table.define(idName, idType, self._toKind(keyword))
        # self.vm_writer.writePush(self._toSegment(idKind), self._indexOf(idName))
        while self.tokenizer.symbol() == ',':
            self.process(',')
            idName = self.tokenizer.identifier()
            self.process(self.tokenizer.identifier())
            self._class_table.define(idName, idType, self._toKind(keyword))
            # self.vm_writer.writePush(self._toSegment(idKind), self._indexOf(idName))
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</classVarDec>')
    
    def compileSubroutineDec(self):
        self.printXMLTag('<subroutineDec>')
        self._tab_count += 1
        self.process(['constructor', 'function', 'method'])
        types = self.get_types()
        types.append('void')
        self.process(types)
        funcName = self.tokenizer.identifier()
        self.process(self.tokenizer.identifier())
        self.process('(')
        nVars = 0
        if self.tokenizer.tokenType() in ['IDENTIFIER', 'KEYWORD']:
            nVars = self.compileParameterList()
        self.process(')')
        self.vm_writer.writeFunction(self._getFunctionName(funcName), nVars)
        self.compileSubroutineBody()
        self._tab_count -= 1
        self.printXMLTag('</subroutineDec>')
    
    def compileParameterList(self):
        self.printXMLTag('<parameterList>')
        self._tab_count += 1
        count = 0
        if not self.tokenizer.symbol() == ')':
            count += 1
        idType = self.tokenizer.keyWord() or self.tokenizer.identifier()
        self.process(self.get_types())
        idName = self.tokenizer.identifier()
        self.process(self.tokenizer.identifier())
        self._method_table.define(idName, idType, 'argument')
        while self.tokenizer.symbol() == ',':
            count += 1
            self.process(',')
            idType = self.tokenizer.keyWord() or self.tokenizer.identifier()
            self.process(self.get_types())
            idName = self.tokenizer.identifier()
            self.process(self.tokenizer.identifier())
            self._method_table.define(idName, idType, 'argument')
        self._tab_count -= 1
        self.printXMLTag('</parameterList>')
        return count

    def compileSubroutineBody(self):
        self.printXMLTag('<subroutineBody>')
        self._tab_count += 1
        self.process('{')
        while self.tokenizer.keyWord() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.process('}')
        self._tab_count -= 1
        self.printXMLTag('</subroutineBody>')
    
    def compileVarDec(self):
        self.printXMLTag('<varDec>')
        self._tab_count += 1
        self.process('var')
        idType = self.tokenizer.keyWord() or self.tokenizer.identifier()
        self.process(self.get_types())
        idName = self.tokenizer.identifier()
        self.process(self.tokenizer.identifier())
        self._method_table.define(idName, idType, 'local')
        while self.tokenizer.symbol() == ',':
            self.process(',')
            idName = self.tokenizer.identifier()
            self.process(self.tokenizer.identifier())
            self._method_table.define(idName, idType, 'local')
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</varDec>')

    def compileStatements(self):
        self.printXMLTag('<statements>')
        self._tab_count += 1
        while self.tokenizer.keyWord() in ['let', 'if', 'while', 'do', 'return']:
            match self.tokenizer.keyWord():
                case 'let':
                    self.compileLet()
                case 'if':
                    self.compileIf()
                case 'while':
                    self.compileWhile()
                case 'do':
                    self.compileDo()
                case 'return':
                    self.compileReturn()
        self._tab_count -= 1
        self.printXMLTag('</statements>')

    def compileLet(self):
        self.printXMLTag('<letStatement>')
        self._tab_count += 1
        self.process('let')
        varName = self.tokenizer.identifier()
        self.process(self.tokenizer.identifier())
        if self.tokenizer.symbol() == '[':
            self.process('[')
            self.compileExpression()
            self.process(']')
        self.process('=')
        self.compileExpression()
        self.vm_writer.writePop(self._kindOf(varName), self._indexOf(varName))
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</letStatement>')
    
    def compileIf(self):
        self.printXMLTag('<ifStatement>')
        self._tab_count += 1
        self.process('if')
        self.process('(')
        self.compileExpression()
        self.process(')')
        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf('L1')
        self.process('{')
        self.vm_writer.writeLabel('L1')
        self.compileStatements()
        self.vm_writer.writeGoto('L2')
        self.process('}')
        self.vm_writer.writeLabel('L2')
        if self.tokenizer.keyWord() == 'else':
            self.process('else')
            self.process('{')
            self.compileStatements()
            self.process('}')
        self._tab_count -= 1
        self.printXMLTag('</ifStatement>')

    def compileWhile(self):
        self.printXMLTag('<whileStatement>')
        self._tab_count += 1
        self.process('while')
        self.process('(')
        self.vm_writer.writeLabel('L1')
        self.compileExpression()
        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf('L2')
        self.process(')')
        self.process('{')
        self.compileStatements()
        self.vm_writer.writeGoto('L1')
        self.process('}')
        self.vm_writer.writeLabel('L2')
        self._tab_count -= 1
        self.printXMLTag('</whileStatement>')

    def compileDo(self):
        self.printXMLTag('<doStatement>')
        self._tab_count += 1
        self.process('do')
        self.compileExpression()
        self.vm_writer.writePop('temp', 0)
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</doStatement>')

    def compileReturn(self):
        self.printXMLTag('<returnStatement>')
        self._tab_count += 1
        self.process('return')
        if self.tokenizer.symbol() != ';':
            self.compileExpression()
        else:
            self.vm_writer.writePush('constant', 0)
        self.vm_writer.writeReturn()
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</returnStatement>')

    def compileExpression(self):
        self.printXMLTag('<expression>')
        self._tab_count += 1
        self.compileTerm()
        while self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            binaryOp = self.tokenizer.symbol()
            self.process(self.tokenizer.symbol())
            self.compileTerm()
            self.vm_writer.writeArithmetic(self._binary_ops.get(binaryOp))
        self._tab_count -= 1
        self.printXMLTag('</expression>')
    
    def compileTerm(self):
        self.printXMLTag('<term>')
        self._tab_count += 1
        match self.tokenizer.tokenType():
            case 'INT_CONST':
                self.vm_writer.writePush('constant', self.tokenizer.intVal())
                self.process(self.tokenizer.intVal())
            case 'STRING_CONST':
                self.vm_writer.writePush('constant', self.tokenizer.stringVal())
                self.process(self.tokenizer.stringVal())
            case 'KEYWORD':
                if self.tokenizer.keyWord() in ['true', 'false', 'null', 'this']:
                    match self.tokenizer.keyWord():
                        case 'true':
                            self.vm_writer.writePush('constant', 1)
                            self.vm_writer.writeArithmetic('neg')
                        case 'false':
                            self.vm_writer.writePush('constant', 0)
                        case 'null':
                            self.vm_writer.writePush('constant', 0)
                        case 'this':
                            self.vm_writer.writePush('pointer', 0)
                    self.process(self.tokenizer.keyWord())
                elif self.tokenizer.keyWord() == 'do':
                    self.process('do')
                    self.compileTerm()
            case 'IDENTIFIER':
                identifier = self.tokenizer.identifier()
                self.process(identifier)

                if self.tokenizer.tokenType() == 'SYMBOL':
                    match self.tokenizer.symbol():
                        case '[':
                            self.process('[')
                            self.compileExpression()
                            self.process(']')
                        case '(':
                            # push method
                            self.process('(')
                            nArgs = self.compileExpressionList()
                            self.process(')')
                            self.vm_writer.writeCall(self._getFunctionName(identifier), nArgs)
                            self._method_class = ''
                        case '.':
                            if self._typeOf(identifier):
                                self._method_class = self._typeOf(identifier)
                            else:
                                self._method_class = identifier
                            self.process('.')
                            self.compileTerm()
                        case _:
                            if self._typeOf(identifier):
                                self.vm_writer.writePush(self._kindOf(identifier), self._indexOf(identifier))

            case 'SYMBOL':
                match self.tokenizer.symbol():
                    case '(':
                        self.process('(')
                        self.compileExpression()
                        self.process(')')
                    case '-' | '~':
                        unaryOp = self.tokenizer.symbol()
                        self.process(self.tokenizer.symbol())
                        self.compileTerm()
                        self.vm_writer.writeArithmetic(self._unary_ops.get(unaryOp))

        self._tab_count -= 1
        self.printXMLTag('</term>')

    def compileExpressionList(self):
        self.printXMLTag('<expressionList>')
        self._tab_count += 1
        count = 0
        if not self.tokenizer.symbol() == ')':
            count += 1
        self.compileExpression()
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.compileExpression()
            count += 1
        self._tab_count -= 1
        self.printXMLTag('</expressionList>')
        return count

    def _kindOf(self, name):
        for symbol_table in [self._method_table, self._class_table]:
            kind = symbol_table.kindOf(name)
            if not kind == '':
                return kind
        return ''

    def _typeOf(self, name):
        for symbol_table in [self._method_table, self._class_table]:
            idType = symbol_table.typeOf(name)
            if not idType == '':
                return idType
        return ''

    def _indexOf(self, name):
        for symbol_table in [self._method_table, self._class_table]:
            i = symbol_table.indexOf(name)
            if i > -1:
                return i
        return ''

    def _getFunctionName(self, identifier):
        if self._method_class:
            return self._method_class + '.' + identifier
        elif self._curr_class:
            return self._curr_class + '.' + identifier

    def _toKind(self, keyword):
        match keyword:
            case 'local':
                return 'local'
            case 'argument' | 'ARG':
                return 'argument'
            case 'static':
                return 'static'
            case 'field':
                return 'this'
            case _:
                print(keyword)