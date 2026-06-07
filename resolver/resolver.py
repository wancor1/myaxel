# SPDX-License-Identifier: MPL-2.0

import data.const as const
import data.store as store
import data.data as data
import util.util as util

class Resolver:
    def __init__(self,ast:data.Program) -> None:
        self.ast:data.Program=ast
        self.scope_stuck:list[dict[str,dict[str,object]]]=[{}]
        self.in_function:bool=False
        self.in_loop:bool=False
        self.errors:list=[]

    def error(self,type:str,**kwargs) -> None:
        if type=='NotFoundVariable':    self.errors.append(data.ErrorFormatAST(type,f'{kwargs['name']} is not a valid variable name'))
        if type=='TooManyLet':          self.errors.append(data.ErrorFormatAST(type,f'{kwargs['name']} is already declared in this scope'))
        if type=='TooManyFn':           self.errors.append(data.ErrorFormatAST(type,f'{kwargs['name']} is already defined in this scope'))

    def scope_push(self):
        self.scope_stuck.append({})

    def scope_pop(self):
        self.scope_stuck.pop()

    def scope_serch(self,name):
        s=reversed(self.scope_stuck)
        for i in s:
            if name in i: return i[name]
        return self.error('NotFoundVariable',name=name)

    def main(self):
        for node in self.ast.statements:
            if store.debug: print(node)
            if isinstance(node,data.Let):
                if node.name not in self.scope_stuck[-1]: self.scope_stuck[-1][node.name]={'type':node.type_,'mutable':node.mutable}
                else: self.error('TooManyLet',name=node.name)
            elif isinstance(node,data.Fn):
                if node.name not in self.scope_stuck[-1]: self.scope_stuck[-1][node.name]={'type':'fn','mutable':False}
                else: self.error('TooManyFn',name=node.name)
        for node in self.ast.statements:
            pass
        return self.errors
