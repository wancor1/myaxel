from dataclasses import dataclass
from typing import Any,Sequence

@dataclass
class Token:
    type:str
    value:str|int
    line:int
    column:int

@dataclass
class ErrorFormat:
    type:str
    text:str
    line:int
    column:int
    needed:str|None=None
    endline:int=-1
    endcol:int=-1
    def __post_init__(self):
        if self.endline == -1: self.endline = self.line
        if self.endcol == -1: self.endcol = self.column

# ==========

@dataclass
class Program:
    statements:list

@dataclass
class Let:
    name:str
    value:Expr|None
    mutable:bool
    overflow:str
    type_:str

@dataclass
class If:
    condition:Expr
    body:list
    else_:Any|None

@dataclass
class Fn:
    name:str
    params:Sequence[Parm|None]
    return_type:str|None
    body:list

@dataclass
class Parm:
    name:str
    type_:str|None

@dataclass
class Return:
    value:Expr|None

@dataclass
class Expr:
    value:list

@dataclass
class Literal:
    value:Any

@dataclass
class Variable:
    name:Any

@dataclass
class Binary:
    left:Any
    op:Any
    right:Any

@dataclass
class Assign:
    name:str
    value:Expr

# ==========
