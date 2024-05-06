type Kind = tuple['STATIC', 'FIELD', 'ARG', 'VAR']

class SymbolTable():
    def __init__(self):
        self._identifiers = []
    
    def reset(self):
        self._identifiers = []
    
    def define(self, name, type, kind: Kind):
        self._identifiers.append({'name': name, 'type': type, 'kind': kind})
    
    def varCount(self, kind: Kind) -> int:
        count = 0
        for identifier in self._identifiers:
            if identifier['kind'] == kind:
                count += 1
        return count

    def kindOf(self, name) -> Kind:
        for identifier in self._identifiers:
            if identifier('name') == name:
                return identifier('kind')
    
    def typeOf(self, name) -> str:
        for identifier in self._identifiers:
            if identifier('name') == name:
                return identifier('type')

    def indexOf(self, name) -> int:
        return self._identifiers.index(name)
