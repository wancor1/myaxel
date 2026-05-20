class BreakException(Exception): pass

class ContinueException(Exception): pass

class ReturnException(Exception):
    def __init__(self,value): self.value=value

class UndefinedVariableException(Exception):
    def __init__(self,name): self.name=name
