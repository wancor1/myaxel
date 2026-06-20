# SPDX-License-Identifier: MPL-2.0


class UnknownException(Exception):
    def __init__(self,value): self.value=value

# environment

class UndefinedVariableException(Exception):
    def __init__(self,name): self.name=name

class UnknownVariableKeyException(Exception):
    def __init__(self,key): self.key=key

# interpreter

class BreakException(Exception): pass

class ContinueException(Exception): pass

class ReturnException(Exception):
    def __init__(self,value) -> None: self.value=value

class NotFindBraces(Exception):
    def __init__(self,value) -> None: self.value=value

class UndefinedBinaryException(Exception):
    def __init__(self,name) -> None: self.name=name

class Div0(Exception):
    def __init__(self,value) -> None: self.value=value
