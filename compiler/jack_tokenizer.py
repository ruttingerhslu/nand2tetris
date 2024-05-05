import re

class JackTokenizer:
    comment_re = re.compile(
        r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )

    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

    def __init__(self, file):
        self._file = file
        self._tokens = []
        self._file_to_tokens(file)
        self._curr_index = -1
    
    def hasMoreTokens(self):
        return len(self._tokens) - 1 > self._curr_index

    def advance(self):
        self._curr_index += 1
        return self._tokens[self._curr_index]

    def tokenType(self):
        token = self._tokens[self._curr_index]
        if token in self.keywords:
            return 'KEYWORD'
        elif token in self.symbols:
            return 'SYMBOL'
        elif token.isdigit() and 0 <= int(token) <= 32767:
            return 'INT_CONST'
        elif token.startswith('\"'):
            return 'STRING_CONST'
        elif token.isidentifier() and not token[0].isdigit():
            return 'IDENTIFIER'
        else:
            return 'UNKNOWN'
    
    def keyWord(self):
        if self.tokenType() == 'KEYWORD':
            return self.tokens[self._curr_index]
        return ''

    def symbol(self):
        if self.tokenType() == 'SYMBOL':
            return self.tokens[self._curr_index]
        return ''
    
    def identifier(self):
        if self.tokenType() == 'IDENTIFIER':
            return self.tokens[self._curr_index]

    def intVal(self):
        if self.tokenType() == 'INT_CONST':
            return self.tokens[self._curr_index]

    def stringVal(self):
        if self.tokenType() == 'STRING_CONST':
            return self.tokens[self._curr_index]

    def _file_to_tokens(self, file):
        file = open(file, 'r')
        file_content = self._remove_comments(file.read())
        lines = [line for line in file_content.split('\n') if line]

        for line in lines:
            string_tokens = self._delimit_string(line)
            for token in string_tokens:
                if token.startswith("\""):
                    self._append_token(token)
                else:
                    delimited_tokens = self._delimit_space(token)
                    for delimited_token in delimited_tokens:
                        if delimited_token:
                            if any(symbol in delimited_token for symbol in self.symbols):
                                self._delimit_symbol(delimited_token)
                            elif any(keyword in delimited_token for keyword in self.keywords):
                                self._delimit_keyword(delimited_token)
                            elif delimited_token.isidentifier() or delimited_token.isdigit():
                                self._append_token(delimited_token)

    def _delimit_string(self, token):
        return re.split(r'(\"[^"]+\")', token)

    def _delimit_space(self, token):
        token = token.strip()
        tokens = token.split(' ')
        return [token.replace(" ", "") for token in tokens]

    def _delimit_symbol(self, token):
        pattern = "(" + "|".join(re.escape(symbol) for symbol in self.symbols) + ")"
        parts = re.split(pattern, token)
        parts = [part for part in parts if part]
        self._append_token(parts)

    def _delimit_keyword(self, token):
        pattern = "(" + "|".join(re.escape(keyword) for keyword in self.keywords) + ")"
        parts = re.split(pattern, token)
        parts = [part for part in parts if part]
        self._append_token(parts)

    def _append_token(self, token):
        if (isinstance(token, list)):
            self._tokens.extend(token)
        elif token != '':
            self._tokens.append(token)

    def _remove_comments(self, string):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
        def _replacer(match):
            if match.group(2) is not None:
                return ""
            else:
                return match.group(1)
        return regex.sub(_replacer, string)