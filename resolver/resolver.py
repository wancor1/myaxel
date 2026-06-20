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
        elif type=='NotFn':             self.errors.append(data.ErrorFormatAST(type,f'not inside the function'))
        elif type=='NotLoop':           self.errors.append(data.ErrorFormatAST(type,f'not inside the loop'))
        elif type=='UnknownNode':       self.errors.append(data.ErrorFormatAST(type,f'Unknown Node: {kwargs['node']}'))
        else :                          self.errors.append(data.ErrorFormatAST(type,f'Unknown Error'))
        if store.debug: print(f'\033[38;5;196m>> {type};{kwargs}\033[0m')

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
        elif isinstance(node,data.While): self.resolve_while(node)
        elif isinstance(node,data.Assign): self.resolve_assign(node)
        elif isinstance(node,data.Expr): self.resolve_expr(node)
        elif isinstance(node,data.Binary): self.resolve_binary(node)
        elif isinstance(node,data.Unary): self.resolve_unary(node)
        elif isinstance(node,data.Call): self.resolve_call(node)
        elif isinstance(node,data.Index): self.resolve_index(node)
        elif isinstance(node,data.MethodCall): self.resolve_methodcall(node)
        elif isinstance(node,data.Return): self.resolve_return(node)
        elif isinstance(node,data.Break): self.resolve_breakcontinue()
        elif isinstance(node,data.Continue): self.resolve_breakcontinue()
        elif isinstance(node,list): self.twopass(node)
        # elif isinstance(node,data.Literal): return
        # elif isinstance(node,data.Use): return
        # elif isinstance(node,data.Import): return
        else: return # self.error('UnknownNode',node=node)

    def resolve_let(self,node:data.Let):
        if len(self.scope_stuck)>1:
            if node.name not in self.scope_stuck[-1]: self.scope_stuck[-1][node.name]={'type':node.type_,'mutable':node.mutable}
            else: self.error('TooManyLet',name=node.name)
        self.resolve(node.value)
        if store.debug: print(f'\033[38;5;244m>stuck {self.scope_stuck}\033[0m')

    def resolve_fn(self,node:data.Fn):
        self.in_function=True
        self.scope_push()
        if store.debug: print(f'\033[38;5;244m>params {node.params}\033[0m')
        for _ in node.params:
            if not _: continue
            self.scope_stuck[-1][_.name]={'type':_.type_ if _.type_ else 'any','mutable':False}
        if store.debug:
            print(f'\033[38;5;244m>body {node.body}\033[0m')
            print(f'\033[34m==================== fn {node.name} ====================',end='\033[0m')
        self.twopass(node.body)
        if store.debug: print(f'\033[34m======================{"="*(len(node.name)+1)}======================\033[0m')
        self.scope_pop()
        self.in_function=False

    def resolve_if(self,node:data.If):
        if store.debug: print(f'\033[38;5;244m>condition {node.condition}\033[0m')
        self.resolve(node.condition)
        if store.debug:
            print(f'\033[38;5;244m>body {node.body}\033[0m')
            print(f'\033[34m==================== If body ====================',end='\033[0m')
        self.scope_push()
        self.twopass(node.body)
        self.scope_pop()
        if store.debug: print(f'\033[34m================================================\033[0m')
        if node.else_:
            if store.debug:
                print(f'\033[38;5;244m>else {node.else_}\033[0m')
                print(f'\033[34m==================== If else ====================',end='\033[0m')
            self.scope_push()
            self.twopass(node.else_)
            self.scope_pop()
            if store.debug: print(f'\033[34m=================================================\033[0m')

    def resolve_while(self,node:data.While):
        self.in_loop=True
        if store.debug: print(f'\033[38;5;244m>condition {node.condition}\033[0m')
        self.resolve(node.condition)
        if store.debug:
            print(f'\033[38;5;244m>body {node.body}\033[0m')
            print(f'\033[34m==================== While body ====================',end='\033[0m')
        self.scope_push()
        self.twopass(node.body)
        if store.debug: print(f'\033[34m===================================================\033[0m')
        self.scope_pop()
        self.in_loop=False

    def resolve_assign(self,node:data.Assign):
        self.scope_serch(node.name)
        self.resolve(node.value)

    def resolve_expr(self,node:data.Expr):
        self.twopass(node.value)

    def resolve_binary(self,node:data.Binary):
        self.resolve(node.left)
        self.resolve(node.right)

    def resolve_unary(self,node:data.Unary):
        self.resolve(node.operand)

    def resolve_call(self,node:data.Call):
        self.twopass(node.args)

    def resolve_index(self,node:data.Index):
        self.resolve(node.array)
        self.resolve(node.index)

    def resolve_methodcall(self,node:data.MethodCall):
        self.resolve(node.obj)
        self.twopass(node.args)

    def resolve_return(self,node:data.Return):
        if not self.in_function: self.error('NotFn')
        if node.value: self.resolve(node.value)

    def resolve_breakcontinue(self):
        if not self.in_loop: self.error('NotLoop')

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
        if store.debug: print('\033[36m> 1pass\033[0m')
        self.onepass(nd)
        if self.errors: return self.errors
        if store.debug: print(f'\033[35m{self.scope_stuck}\n\033[36m> 2pass\033[0m')
        self.twopass(nd)
        return self.errors
