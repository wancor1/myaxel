# SPDX-License-Identifier: MPL-2.0

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

@dataclass
class ErrorFormatAST:
    type:str
    text:str
    needed:str|None=None

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
    else_:list

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

@dataclass
class Import:
    path:str

@dataclass
class Use:
    module:str
    name:str

# ===

@dataclass
class Program:
    statements:list[x]

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
    fs:bool=False

@dataclass
class Variable:
    name:str

@dataclass
class Binary:
    left:x
    op:str
    right:x

@dataclass
class Assign:
    name:str
    value:Expr

@dataclass
class CompoundAssign:
    name:str
    value:Expr
    op:str

@dataclass
class Unary:
    op:str
    operand:x

@dataclass
class Access:
    obj:str
    member:str

@dataclass
class MethodCall:
    obj: x
    method: str
    args: list

@dataclass
class Array:
    elements:list

@dataclass
class Index:
    array:x
    index:Expr

# ==========

x=Literal|Variable|Binary|Call|Unary|Array|Access|MethodCall|Index
a=Call|Parm|Expr|Literal|Variable|Binary|Assign|CompoundAssign|Unary|Access|MethodCall|Array|Index|Let|If|Fn|Break|Return|While|Use
