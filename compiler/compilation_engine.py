from jack_tokenizer import JackTokenizer

class CompilationEngine:
    _identifier_names = {
        'class': [],
        'subroutine': [],
        'var': []
    }

    def __init__(self, read_file, write_file, class_names):
        self._read_file = read_file
        self._write_file = open(write_file, 'w')

        self.tokenizer = JackTokenizer(read_file)
        self._curr_token = self.tokenizer.advance()
        
        self._identifier_names['class'] = class_names

        print(self._identifier_names)
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
            return self._identifier_names['class']
        elif self.tokenizer.tokenType() == 'KEYWORD':
            return ['int', 'char', 'boolean']
        else:
            return ''
    
    def process_identifier(self, category):
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            self._identifier_names[category].append(self.tokenizer.identifier())
            self.process(self._identifier_names[category])
        else: print('syntax error')
    
    def compileClass(self):
        self.printXMLTag('<class>')
        self.process('class')
        self.process_identifier('class')
        self.process('{')
        while self.tokenizer.keyWord() in ['static', 'field']:
            self.compileClassVarDec()
        while self.tokenizer.keyWord() in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
        self.printXMLTag('</class>')

    def compileClassVarDec(self):
        self.printXMLTag('<classVarDec>')
        self.process(['static', 'field'])
        self.process(self.get_types())
        self.process_identifier('var')
        while self.tokenizer.symbol == ',':
            self.process(',')
            self.process_identifier('var')
        self.process(';')
        self.printXMLTag('</classVarDec>')
    
    def compileSubroutineDec(self):
        self.printXMLTag('<subroutineDec>')
        self.process(['constructor', 'function', 'method'])
        self.process(['void', self.get_types()])
        self.process_identifier('subroutine')
        self.process('(')
        self.compileParameterList()
        self.process(')')
        self.compileSubroutineBody()
        self.printXMLTag('</subroutineDec>')
    
    def compileParameterList(self):
        if self.tokenizer.tokenType() in ['IDENTIFIER', 'KEYWORD']:
            self.printXMLTag('<parameterList>')
            self.process(self.get_types())
            self.process_identifier('var')
            while self.tokenizer.symbol == ',':
                self.process(',')
                self.process(self.get_types())
                self.process_identifier('var')
            self.process(';')
            self.printXMLTag('</parameterList>')

    def compileSubroutineBody(self):
        self.printXMLTag('<subroutineBody>')
        self.process('{')
        while self.tokenizer.keyWord() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.printXMLTag('</subroutineBody>')
    
    def compileVarDec(self):
        self.printXMLTag('<varDec>')
        self.process('var')
        self.process(self.get_types())
        self.process_identifier('var')
        print('symbol: ', self.tokenizer.symbol())
        while self.tokenizer.symbol() == ',':
            self.process(',')
            self.process_identifier('var')
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
        self.process_identifier('var')
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
                    self.compileSubroutineCall()
            case 'IDENTIFIER':
                if self.tokenizer.identifier() in self._identifier_names['var']:
                    self.process(self._identifier_names['var'])
                    if self.tokenizer.symbol() == '[':
                        self.process('[')
                        self.compileExpression()
                        self.process(']')
                elif self.tokenizer.identifier() in self._identifier_names['subroutine']:
                    self.compileSubroutineCall()
            case 'SYMBOL':
                if self.tokenizer.symbol() == '(':
                    self.process('(')
                    self.compileExpression()
                    self.process(')')
                elif self.tokenizer.symbol() in ['-', '~']:
                    self.process(self.tokenizer.symbol())
                    self.compileTerm()
        self.printXMLTag('</term>')

    def compileSubroutineCall(self):
        if (self._identifier_names['class']):
            self.process(self._identifier_names['class'])
            self.process('.')
        elif (self._identifier_names['var']):
            self.process(self._identifier_names['var'])
            self.process('.')
        self.process(self._identifier_names['subroutine'])
        self.process('(')
        self.compileExpressionList()
        self.process(')')

    def compileExpressionList(self):
        self.printXMLTag('<expressionList>')
        self.compileExpression()
        while self.tokenizer.symbol == ',':
            self.process(',')
            self.compileExpression()
        self.printXMLTag('</expressionList>')
