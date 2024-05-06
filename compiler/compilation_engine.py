from jack_tokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, read_file, write_file):
        self._read_file = read_file
        self._write_file = open(write_file, 'w')

        self.tokenizer = JackTokenizer(read_file)
        self._curr_token = self.tokenizer.advance()

        self._last_token = ''

        self._tab_count = 0

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
        self.process(self.tokenizer.identifier())
        self.process('{')
        while self.tokenizer.keyWord() in ['static', 'field']:
            self.compileClassVarDec()
        while self.tokenizer.keyWord() in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
        self.process('}')
        self._tab_count -= 1
        self.printXMLTag('</class>')

    def compileClassVarDec(self):
        self.printXMLTag('<classVarDec>')
        self._tab_count += 1
        self.process(['static', 'field'])
        self.process(self.get_types())
        self.process(self.tokenizer.identifier())
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.process(self.tokenizer.identifier())
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
        self.process(self.tokenizer.identifier())
        self.process('(')
        self.compileParameterList()
        self.process(')')
        self.compileSubroutineBody()
        self._tab_count -= 1
        self.printXMLTag('</subroutineDec>')
    
    def compileParameterList(self):
        if self.tokenizer.tokenType() in ['IDENTIFIER', 'KEYWORD']:
            self.printXMLTag('<parameterList>')
            self._tab_count += 1
            self.process(self.get_types())
            self.process(self.tokenizer.identifier())
            while self.tokenizer.symbol() == ',':
                self.process(',')
                self.process(self.get_types())
                self.process(self.tokenizer.identifier())
            self._tab_count -= 1
            self.printXMLTag('</parameterList>')

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
        self.process(self.get_types())
        self.process(self.tokenizer.identifier())
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.process(self.tokenizer.identifier())
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
        self.process(self.tokenizer.identifier())
        if self.tokenizer.symbol() == '[':
            self.process('[')
            self.compileExpression()
            self.process(']')
        self.process('=')
        self.compileExpression()
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
        self.process('{')
        self.compileStatements()
        self.process('}')
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
        self.compileExpression()
        self.process(')')
        self.process('{')
        self.compileStatements()
        self.process('}')
        self._tab_count -= 1
        self.printXMLTag('</whileStatement>')

    def compileDo(self):
        self.printXMLTag('<doStatement>')
        self._tab_count += 1
        self.process('do')
        self.compileExpression()
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</doStatement>')

    def compileReturn(self):
        self.printXMLTag('<returnStatement>')
        self._tab_count += 1
        self.process('return')
        if self.tokenizer.symbol() != ';':
            self.compileExpression()
        self.process(';')
        self._tab_count -= 1
        self.printXMLTag('</returnStatement>')

    def compileExpression(self):
        self.printXMLTag('<expression>')
        self._tab_count += 1
        self.compileTerm()
        while self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.process(self.tokenizer.symbol())
            self.compileTerm()
        self._tab_count -= 1
        self.printXMLTag('</expression>')
    
    def compileTerm(self):
        self.printXMLTag('<term>')
        self._tab_count += 1
        match self.tokenizer.tokenType():
            case 'INT_CONST':
                self.process(self.tokenizer.intVal())
            case 'STRING_CONST':
                self.process(self.tokenizer.stringVal())
            case 'KEYWORD':
                if self.tokenizer.keyWord() in ['true', 'false', 'null', 'this']:
                    self.process(self.tokenizer.keyWord())
                elif self.tokenizer.keyWord() == 'do':
                    self.process('do')
                    self.compileTerm()
            case 'IDENTIFIER':
                self._last_token = self.tokenizer.identifier()
                self.process(self.tokenizer.identifier())
                if self.tokenizer.tokenType() == 'SYMBOL':
                    match self.tokenizer.symbol():
                        case '[':
                            self.process('[')
                            self.compileExpression()
                            self.process(']')
                        case '(':
                            self.process('(')
                            self.compileExpressionList()
                            self.process(')')
                        case '.':
                            self.process('.')
                            self.process(self.tokenizer.identifier())
                            self.process('(')
                            self.compileExpressionList()
                            self.process(')')
            case 'SYMBOL':
                if self.tokenizer.symbol() == '(':
                    self.process('(')
                    self.compileExpression()
                    self.process(')')
                elif self.tokenizer.symbol() in ['-', '~']:
                    self.process(self.tokenizer.symbol())
                    self.compileTerm()
        self._tab_count -= 1
        self.printXMLTag('</term>')

    def compileExpressionList(self):
        self.printXMLTag('<expressionList>')
        self._tab_count += 1
        self.compileExpression()
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.compileExpression()
        self._tab_count -= 1
        self.printXMLTag('</expressionList>')
