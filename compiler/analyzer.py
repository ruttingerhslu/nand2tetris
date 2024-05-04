class Analyzer:
    def __init__(self, tokens):
        self._tokens = tokens
        self._file = ''
        self._num_tabs = 0
        self._curr_tag = ''

        # stack of tags class, varDec, etc.
        self.tags = []

        self.classVarNames = []

        self.className = ''

    def analyze(self):
        tabstr = ''
        for token in self._tokens:
            # if token == "class":
            #     self._file += self.get_tabstring() + '<class>\n'
            self.set_tag(token, self.get_category(token))

        # print(self._file)
                
                
    def get_tabstring(self):
        return "\t" * self._num_tabs

    def get_category(self, token):
        keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

        if token in keywords:
            return 'keyword'
        elif token in symbols:
            return 'symbol'
        elif token.isdigit() and 0 <= int(token) <= 32767:
            return 'integerConstant'
        elif token.startswith('\"'):
            return 'StringConstant'
        elif token.isidentifier() and not token[0].isdigit():
            return 'identifier'
        else:
            return 'Unknown'
    
    def set_tag(self, token, category):
        # tag enclosure
        if token == 'class':
            self._curr_tag = 'class'
        elif token in ['constructor', 'function', 'method']:
            self._curr_tag = 'subroutine'
        elif token == 'var':
            self._curr_tag = 'varDec'
            self.tags.append(self._curr_tag)
        elif token == '{':
            # push current tag to tags stack
            self.tags.append(self._curr_tag)
            # print(self.tags[-1])
        elif token == '}':
            # print(self.tags[-1])
            # pop current tag from tags stack
            self.tags.pop()
        elif token == ';' and self._curr_tag == 'varDec':
            self.tags.pop()
            self._curr_tag = ''
        print(self.tags, token, self._curr_tag)

        # # check if varDec:
        # elif token == 'var':
        #     self._curr_dec = 'varDec'
        # # check if subroutineDec:
        # elif token in ['constructor', 'function', 'method']:
        #     self._curr_dec = 'subroutineDec'

        # elif token == 'type':


        # elif (category == 'identifier'):
        #     match self._curr_dec:
        #         case 'class':
        #             self.className = token
        #         case 'subroutineDec':
        #             self.subroutineName = token
        #         case 'classVarDec':
        #             self.classVarNames.append(token)
        # # check if vardec
    def is_type(self, token):
        return token in 'int', 'char', 'boolean', self.className


    def is_expression(self, token, category):
        if token in []:
            return True
        elif :
            return True
            return True
        elif token in ['+', '-', '*', '/', '&', '|', '<', '>' , '=']:
            return True
        else:
            return False

    def is_term(self, token, category):
        return category in ['integerConstant', 'StringConstant'] or self.is_keyword_constant()

    def is_op(self, token):
        return token in ['+', '-', '*', '/', '&', '|', '<', '>' , '=']

    def is_unary_op(self, token):
        return token in ['-', '~']

    def is_keyword_constant(self, token):
        return token in ['true', 'false', 'null', 'this']