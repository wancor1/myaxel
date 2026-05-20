from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

@dataclass
class Token:
    type:str
    value:str
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
    else_:list|None

@dataclass
class Fn:
    name:str
    params:Sequence[Parm|None]
    return_type:str|None
    body:list

@dataclass
class Break:
    pass

@dataclass  
class Continue:
    pass

@dataclass
class Return:
    value:Expr|None

@dataclass
class While:
    condition:Expr
    body:list

# ===

@dataclass
class Program:
    statements:list

@dataclass
class Call:
    name:str
    args:list

@dataclass
class Parm:
    name:str
    type_:str

@dataclass
class Expr:
    value:list

@dataclass
class Literal:
    value:str

@dataclass
class Variable:
    name:str

@dataclass
class Binary:
    left:Literal|Variable|Binary|Call|Unary
    op:str
    right:Literal|Variable|Binary|Call|Unary

@dataclass
class Assign:
    name:str
    value:Expr

@dataclass
class Unary:
    op:str
    operand:Literal|Variable|Binary|Call|Unary

# ==========
