from os import path
import os
import sys
from compilation_engine import CompilationEngine
from jack_tokenizer import JackTokenizer

class JackCompiler:
    def __init__(self, path):
        self._path = path
        self._write_file = ''
        self._read_file = ''

    def compile(self):
        files = self._getJackFiles()
        for file in files:
            self._read_file = file
            self._write_file = file[:file.rfind('.jack')] + '.xml'
            self.tokenize()

    def _getJackFiles(self):
        files = []
        if path.isfile(self._path) and self._path.endswith('.jack'):
            files.append(self._path)
        else:
            for (_, _, file) in os.walk(self._path):
                os.chdir(self._path)
                for f in file:
                    if f.endswith('.jack'):
                        files.append(f)
        return files

    def tokenize(self):
        CompilationEngine(self._read_file, self._write_file)

if __name__ == '__main__':
    jack_path = sys.argv[1]

    jackCompiler = JackCompiler(jack_path)
    jackCompiler.compile()