from os import path
import os
import sys
from analyzer import Analyzer
from tokenizer import Tokenizer

class Compiler:
    def __init__(self, path):
        self._path = path
        self._tokens = []

    def compile(self):
        files = self._getJackFiles()
        for file in files:
            self.tokenize(file)

    def _getJackFiles(self):
        files = []
        if path.isfile(self._path):
            files.append(self._path)
        else:
            for (_, _, file) in os.walk(self._path):
                for f in file:
                    if '.jack' in f:
                        files.append(f)
        return files

    def tokenize(self, file):
        tokenizer = Tokenizer(file)
        tokens = tokenizer.tokenize()
        analyzer = Analyzer(tokens)
        analyzer.analyze()

if __name__ == '__main__':
    jack_path = sys.argv[1]

    hack_assembler = Compiler(jack_path)
    hack_assembler.compile()