import json

type Kind = tuple['STATIC', 'FIELD', 'ARG', 'VAR']

class SymbolTable():
    def __init__(self):
        self._identifiers = []
    
    def reset(self):
        self._identifiers = []
    
    def define(self, name, idType, kind: Kind):
        self._identifiers.append({'name': name, 'type': idType, 'kind': kind})
    
    def varCount(self, kind: Kind) -> int:
        count = 0
        for identifier in self._identifiers:
            if identifier['kind'] == kind:
                count += 1
        return count

    def kindOf(self, name) -> Kind:
        for identifier in self._identifiers:
            if identifier['name'] == name:
                return identifier['kind']
        return ''

    def typeOf(self, name) -> str:
        for identifier in self._identifiers:
            if identifier['name'] == name:
                return identifier['type']
        return ''

    def indexOf(self, name) -> int:
        for i, identifier in enumerate(self._identifiers):
            if identifier['kind'] == self.kindOf(name) and identifier['name'] == name:
                return i
        return -1
    
    def toString(self) -> str:
        return json.dumps(self._identifiers)
