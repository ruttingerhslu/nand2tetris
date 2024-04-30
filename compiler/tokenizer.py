import re

class Tokenizer:
    comment_re = re.compile(
        r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )

    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

    def __init__(self, file):
        self._file = file
        self._tokens = []

    def tokenize(self):
        file = open(self._file, 'r')
        content = self.remove_comments(file.read())
        lines = self.get_lines(content)
        token = ''
        tokens = []
        for line in lines:
            # split for string first
            line_tokens = re.split(r'(\"[^"]+\")', line)
            for token in line_tokens:
                # a string
                if token.startswith("\""):
                    tokens.append(token)
                else:
                    if any(symbol in token for symbol in self.symbols):
                        pattern = '|'.join(map(re.escape, self.symbols))
                        new_tokens = re.split(pattern, token)
                    else:
                        token_tokens = token.split(" ")
                        tokens.append(token_tokens)
                    
                
            print(line_tokens)

        # for char in content:
        #     char = char.strip()
        #     if char in self.symbols:
        #         tokens.append(token) # stringconstant
        #         tokens.append(char) # symbol
        #         token = ''
        #         continue
        #     token = token + char
        #     if token in self.keywords:
        #         tokens.append(token) # keyword
        #         token = ''
        # return tokens
        # tokens = []
        # for line in content.splitlines():
        #     for token in line.split(' '):
        #         token = token.strip()
        #         if (token != ''):
        #             tokens.append(token)
        # return tokens

    def comment_replacer(self, match):
        start,mid,end = match.group(1,2,3)
        if mid is None:
            # single line comment
            return ''
        elif start is not None or end is not None:
            # multi line comment at start or end of a line
            return ''
        elif '\n' in mid:
            # multi line comment with line break
            return ''
        else:
            # multi line comment without line break
            return ''

    def remove_comments(self, text):
        return self.comment_re.sub(self.comment_replacer, text)

    def get_string(self, word):
        return re.match('/\"([^"]+)\"/g', word)
    
    def get_lines(self, text):
        return [line for line in text.split('\n') if line]