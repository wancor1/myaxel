# SPDX-License-Identifier: MPL-2.0

import data.data as data

def increment(ident:str) -> data.Assign:
    return data.Assign(ident,data.Expr([data.Binary(data.Variable(ident),'+',data.Literal('1'))]))

def decrement(ident:str) -> data.Assign:
    return data.Assign(ident,data.Expr([data.Binary(data.Variable(ident),'-',data.Literal('1'))]))

def let(ident:str,literal:data.Expr|str='0',mut:bool=False,of:str='wrap',tp:str='Null') -> data.Let:
    if isinstance(literal,data.Expr): return data.Let(ident,literal,mut,of,tp)
    return data.Let(ident,data.Expr([data.Literal(literal)]),mut,of,tp)
