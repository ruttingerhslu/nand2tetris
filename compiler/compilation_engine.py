from jack_tokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, read_file, write_file):
        with open(write_file, 'r+') as file:
            file.truncate(0)
        self._read_file = read_file
        self._write_file = open(write_file, 'w')

        self.tokenizer = JackTokenizer(read_file)
        self._curr_token = self.tokenizer.advance()

        self._last_token = ''

        self.compileClass()

    def printXMLToken(self, token):
        self._write_file.write('<' + self.tokenizer.tokenType().lower() + '> ' +\
            token +\
            ' </' + self.tokenizer.tokenType().lower() + '>\n')

    def printXMLTag(self, tag):
        self._write_file.write(tag + '\n')

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
        self.process('class')
        self.process(self.tokenizer.identifier())
        self.process('{')
        while self.tokenizer.keyWord() in ['static', 'field']:
            self.compileClassVarDec()
        while self.tokenizer.keyWord() in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
        self.process('}')
        self.printXMLTag('</class>')

    def compileClassVarDec(self):
        self.printXMLTag('<classVarDec>')
        self.process(['static', 'field'])
        self.process(self.get_types())
        self.process(self.tokenizer.identifier())
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.process(self.tokenizer.identifier())
        self.process(';')
        self.printXMLTag('</classVarDec>')
    
    def compileSubroutineDec(self):
        self.printXMLTag('<subroutineDec>')
        self.process(['constructor', 'function', 'method'])
        types = self.get_types()
        types.append('void')
        self.process(types)
        self.process(self.tokenizer.identifier())
        self.process('(')
        self.compileParameterList()
        self.process(')')
        self.compileSubroutineBody()
        self.printXMLTag('</subroutineDec>')
    
    def compileParameterList(self):
        if self.tokenizer.tokenType() in ['IDENTIFIER', 'KEYWORD']:
            self.printXMLTag('<parameterList>')
            self.process(self.get_types())
            self.process(self.tokenizer.identifier())
            while self.tokenizer.symbol() == ',':
                self.process(',')
                self.process(self.get_types())
                self.process(self.tokenizer.identifier())
            self.printXMLTag('</parameterList>')

    def compileSubroutineBody(self):
        self.printXMLTag('<subroutineBody>')
        self.process('{')
        while self.tokenizer.keyWord() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.process('}')
        self.printXMLTag('</subroutineBody>')
    
    def compileVarDec(self):
        self.printXMLTag('<varDec>')
        self.process('var')
        self.process(self.get_types())
        self.process(self.tokenizer.identifier())
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.process(self.tokenizer.identifier())
        self.process(';')
        self.printXMLTag('</varDec>')

    def compileStatements(self):
        self.printXMLTag('<statements>')
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
        self.printXMLTag('</statements>')

    def compileLet(self):
        self.printXMLTag('<letStatement>')
        self.process('let')
        self.process(self.tokenizer.identifier())
        if self.tokenizer.symbol() == '[':
            self.process('[')
            self.compileExpression()
            self.process(']')
        self.process('=')
        self.compileExpression()
        self.process(';')
        # remove identifier
        self.printXMLTag('</letStatement>')
    
    def compileIf(self):
        self.printXMLTag('<ifStatement>')
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
        self.printXMLTag('</ifStatement>')

    def compileWhile(self):
        self.printXMLTag('<whileStatement>')
        self.process('while')
        self.process('(')
        self.compileExpression()
        self.process(')')
        self.process('{')
        self.compileStatements()
        self.process('}')
        self.printXMLTag('</whileStatement>')

    def compileDo(self):
        self.printXMLTag('<doStatement>')
        self.process('do')
        self.compileExpression()
        self.process(';')
        self.printXMLTag('</doStatement>')

    def compileReturn(self):
        self.printXMLTag('<returnStatement>')
        self.process('return')
        self.compileExpression()
        self.process(';')
        self.printXMLTag('</returnStatement>')

    def compileExpression(self):
        self.printXMLTag('<expression>')
        self.compileTerm()
        while self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.process(self.tokenizer.symbol())
            self.compileTerm()
        self.printXMLTag('</expression>')
    
    def compileTerm(self):
        self.printXMLTag('<term>')
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
        self.printXMLTag('</term>')

    def compileExpressionList(self):
        self.printXMLTag('<expressionList>')
        self.compileExpression()
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.compileExpression()
        self.printXMLTag('</expressionList>')
