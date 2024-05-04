class CompilationEngine:
    def __init__(read_file, write_file):
        self._read_file = read_file
        self._write_file = write_file
        self.tokenizer = JackTokenizer(read_file)
        self.compileClass()
        self._curr_token
        self.signature = ''

    def process(self, token):
        if self.tokenizer.hasMoreTokens():
            if (self._curr_token == token):
                self.printXMLToken(token)
            else:
                print('syntax error')
            self._curr_token = self.tokenizer.advance()
        else:
            print('finished program')
    
    def compileClass(self):
        print('<class>')
        self.process('class')

        print('</class>')

    def compileClassVarDec(self):
    
    def compileSubroutine(self):
    
    def compileParameterList(self):

    def compileSubroutineBody(self):
    
    def compileVarDec(self):

    def compileStatements(self):

    def compileLet(self):
    
    def compileIf(self):

    def compileWhile(self):
        print('<whileStatement>')
        self.process('while')
        self.process('(')
        self.compileExpression()
        self.process(')')
        self.process('{')
        self.compileStatements()
        self.process('{')

    def compileDo(self):

    def compileReturn(self):
        print('<returnStatements>')
        self.process('return')
        self.compileExpression()
        self.process(';')
        print('</returnStatements>')

    def compileExpression(self):
        print('<expression>')
        process()
        print('</expression')
    
    def compileTerm(self):
    
    def compileExpressionList(self) -> int:
