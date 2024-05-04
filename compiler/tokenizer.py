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

        for line in lines:
            string_tokens = self._delimit_string(line)
            for string_token in string_tokens:
                if not string_token.startswith("\""):
                    space_tokens = self._delimit_space(string_token)
                    for space_token in space_tokens:
                        if space_token:
                            if any(symbol in space_token for symbol in self.symbols):
                                self._delimit_symbol(space_token)
                            elif any(keyword in space_token for keyword in self.keywords):
                                self._delimit_keyword(space_token)
                            else:
                                self._append_token(space_token)
                else:
                    self._append_token(string_token)
        return self._tokens

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