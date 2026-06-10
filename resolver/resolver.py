# SPDX-License-Identifier: MPL-2.0

import data.const as const
import data.store as store
import data.data as data
import util.util as util

class Resolver:
    def __init__(self) -> None:
        self.scope_stuck:list[dict[str,dict[str,object]]]=[{}]
        self.in_function:bool=False
        self.in_loop:bool=False
        self.errors:list=[]

    def error(self,type:str,**kwargs) -> None:
        if type=='NotFoundVariable':    self.errors.append(data.ErrorFormatAST(type,f'{kwargs['name']} is not a valid variable name'))
        elif type=='TooManyLet':        self.errors.append(data.ErrorFormatAST(type,f'{kwargs['name']} is already declared in this scope'))
        elif type=='TooManyFn':         self.errors.append(data.ErrorFormatAST(type,f'{kwargs['name']} is already defined in this scope'))
        else :                          self.errors.append(data.ErrorFormatAST(type,f'Unknown Error'))

    # ===== scope =====

    def scope_push(self):
        self.scope_stuck.append({})

    def scope_pop(self):
        self.scope_stuck.pop()

    def scope_serch(self,name:str):
        s=reversed(self.scope_stuck)
        for i in s:
            if name in i: return i[name]
        return self.error('NotFoundVariable',name=name)

    # ===== resolve =====

    def resolve(self,node):
        if isinstance(node,data.Variable): self.scope_serch(node.name)
        elif isinstance(node,data.Let): self.resolve_let(node)
        elif isinstance(node,data.Fn): self.resolve_fn(node)
        elif isinstance(node,data.If): self.resolve_if(node)

    def resolve_let(self,node:data.Let):
        if self.in_function:
            if node.name not in self.scope_stuck[-1]: self.scope_stuck[-1][node.name]={'type':node.type_,'mutable':node.mutable}
            else: self.error('TooManyLet',name=node.name)
        self.resolve(node.value)
        print(f'>stuck {self.scope_stuck}')

    def resolve_fn(self,node:data.Fn):
        self.in_function=True
        self.scope_push()
        if store.debug: print(f'>params {node.params}')
        for _ in node.params:
            if not _: continue
            self.scope_stuck[-1][_.name]={'type':_.type_ if _.type_ else 'any','mutable':False}
        if store.debug:
            print(f'>body {node.body}')
            print(f'==================== fn {node.name} ====================',end='')
        self.twopass(node.body)
        if store.debug: print(f'======================{"="*(len(node.name)+1)}======================')
        self.scope_pop()
        self.in_function=False

    def resolve_if(self,node:data.If):
        if store.debug: print(f'>condition {node.condition}')
        self.resolve(node.condition)
        if store.debug:
            print(f'>body {node.body}')
            print(f'==================== If body ====================',end='')
        self.scope_push()
        self.twopass(node.body)
        self.scope_pop()
        if store.debug: print(f'================================================')
        if node.else_:
            if store.debug:
                print(f'>else {node.else_}')
                print(f'==================== If else ====================',end='')
            self.scope_push()
            self.twopass(node.else_)
            self.scope_pop()
            if store.debug: print(f'=================================================')

    # ===== main =====

    def onepass(self,nd):
        for node in nd:
            if store.debug: print(f'> {node}')
            if isinstance(node,data.Let):
                if node.name not in self.scope_stuck[-1]: self.scope_stuck[-1][node.name]={'type':node.type_,'mutable':node.mutable}
                else: self.error('TooManyLet',name=node.name)
            elif isinstance(node,data.Fn):
                if node.name not in self.scope_stuck[-1]: self.scope_stuck[-1][node.name]={'type':'fn','mutable':False}
                else: self.error('TooManyFn',name=node.name)

    def twopass(self,nd):
        for node in nd:
            if store.debug: print(f'\n{node}')
            self.resolve(node)

    def main(self,nd):
        if store.debug: print('> 1pass')
        self.onepass(nd)
        if self.errors: return self.errors
        if store.debug: print(f'{self.scope_stuck}\n> 2pass')
        self.twopass(nd)
        return self.errors
