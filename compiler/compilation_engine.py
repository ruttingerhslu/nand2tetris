class CompilationEngine:
    def __init__(read_file, write_file):
        self._read_file = read_file
        self._write_file = write_file

        self.tokenizer = JackTokenizer(read_file)
        self._curr_token = self.tokenizer.advance()
        self.compileClass()
        self._identifier_names = {
            'class': [],
            'subroutine': [],
            'var': []
        }

    def process(self, tokens):
        if self.tokenizer.hasMoreTokens():
            if (self._curr_token in tokens):
                self.printXMLToken(self._curr_token)
            else:
                print('syntax error')
            self._curr_token = self.tokenizer.advance()
        else:
            print('finished program')
    
    def process_type(self):
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            self.process(self._identifier_stack)
        elif self.tokenizer.tokenType() == 'KEYWORD':
            self.process(['int', 'char', 'boolean'])
        else: print('syntax error')
    
    def process_identifier(self):
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            self._identifier_stack.append(self.tokenizer.identifier())
            self.process(self._identifier_stack)
        else: print('syntax error')

    def remove_identifier(self):
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            self._identifier_stack.pop()
        else: print('syntax error')
    
    def compileClass(self):
        print('<class>')
        self.process(['class'])
        # add classname to list of class names
        self._identifier_names['class'].append(self.tokenizer.identifier())
        self.process(['{'])
        next_keyword = self.tokenizer.keyWord()
        for next_keyword in ['static', 'field']:
            self.compileClassVarDec()
            next_keyword = self.tokenizer.keyWord()
        for next_keyword in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
            next_keyword = self.tokenizer.keyWord()
        print('</class>')

    def compileClassVarDec(self):
        print('<classVarDec>')
        self.process(['static', 'field'])
        self.process_type()
        self.compileVar
        print('</classVarDec>')
    
    def compileSubroutineDec(self):
    
    def compileParameterList(self):

    def compileSubroutineBody(self):
    
    def compileVarDec(self):

    def compileStatements(self):

    def compileLet(self):
    
    def compileIf(self):

    def compileWhile(self):
        print('<whileStatement>')
        self.process(['while'])
        self.process(['('])
        self.compileExpression()
        self.process([')'])
        self.process(['{'])
        self.compileStatements()
        self.process(['{'])

    def compileDo(self):

    def compileReturn(self):
        print('<returnStatements>')
        self.process(['return'])
        self.compileExpression()
        self.process([';'])
        print('</returnStatements>')

    def compileExpression(self):
        print('<expression>')
        process()
        print('</expression')
    
    def compileTerm(self):
    
    def compileExpressionList(self) -> int:
