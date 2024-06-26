class Parser:
    _cmd_types = {
        'C_ARITHMETIC': ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'],
        'C_PUSH': ['push'],
        'C_POP': ['pop'],
        'C_LABEL': ['label'],
        'C_GOTO': ['goto'],
        'C_IF': ['if-goto'],
        'C_FUNCTION': ['function'],
        'C_RETURN': ['return'],
        'C_CALL': ['call'],
    }

    def __init__(self, vm_file):
        file = open(vm_file, 'r')
        self._lines = self._clean_lines(file.readlines())
        self._curr_line = 0
        self._reset()

    def _reset(self):
        self._curr_cmd_type = ''
        self._curr_cmd = ''

    def _clean_lines(self, lines):
        clean_lines = []
        for line in lines:
            if not self._line_empty(line) and not self._line_comment(line):
                clean_lines.append(line.replace('\n', ''))
        return clean_lines

    def _line_empty(self, line):
        return not line.strip()

    def _line_comment(self, line):
        return line.strip().startswith('//')

    def _next_line(self):
        self._curr_line = self._lines.pop(0)
        self._curr_cmd = self._curr_line.split(' ')[0]
        return self._curr_line

    def hasMoreLines(self):
        return self._lines != []

    def advance(self):
        self._reset()
        self._next_line()

        for cmd_type in self._cmd_types:
            if self._curr_cmd in self._cmd_types[cmd_type]:
                self._curr_cmd_type = cmd_type

    def commandType(self):
        return self._curr_cmd_type

    def arg1(self):
        args = self._curr_line.split(' ')
        if self._curr_cmd_type == 'C_ARITHMETIC':
            return args[0]
        else:
            return args[1]
    
    def arg2(self):
        return self._curr_line.split(' ')[2]