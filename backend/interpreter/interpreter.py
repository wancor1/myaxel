# SPDX-License-Identifier: MPL-2.0

import data.data as data
import data.exception as exception
import frontend.lexer as _lexer
import frontend.parser as _parser
import backend.interpreter.environment as environment

import math

class Interpreter:
    def __init__(self):
        self.env=environment.Environment()
        
    def error(self,node,wte:str):
        print(f'{wte}:{node}')

    def eval(self,node):
        if isinstance(node,data.Literal):       return self.eval_literal(node)
        elif isinstance(node,data.Variable):    return self.eval_variable(node)
        elif isinstance(node,data.Expr):        return self.eval(node.value[0])
        elif isinstance(node,data.Binary):
            l=self.eval(node.left)
            r=self.eval(node.right)
            if node.op=='+':    return l+r
            elif node.op=='-':  return l-r
            elif node.op=='*':  return l*r
            elif node.op=='/':  return self.error(node,'div0error') if r==0 else l/r
            elif node.op=='**': return l**r
            elif node.op=='<':  return l<r 
            elif node.op=='>':  return l>r 
            elif node.op=='<=': return l<=r
            elif node.op=='>=': return l>=r
            elif node.op=='==': return l==r
            elif node.op=='!=': return l!=r
        elif isinstance(node,data.Let):         self.env.define(node.name,self.eval(node.value) if node.value else None,node.type_,node.mutable,node.overflow)
        elif isinstance(node,data.Assign):      self.env.set(node.name,self.eval(node.value))
        elif isinstance(node, data.Unary):
            if node.op=='-': return -self.eval(node.operand)
        elif isinstance(node,data.If):
            if self.eval(node.condition):
                for stmt in node.body:  self.eval(stmt)
            elif node.else_:
                for stmt in node.else_: self.eval(stmt)
        elif isinstance(node,data.While):
            while self.eval(node.condition):
                try:
                    for stmt in node.body:
                        if isinstance(stmt,list):
                            for s in stmt: self.eval(s)
                        else: self.eval(stmt)
                except exception.ContinueException: continue
                except exception.BreakException:    break
        elif isinstance(node,data.Break):       raise exception.BreakException(node)
        elif isinstance(node,data.Continue):    raise exception.ContinueException(node)
        elif isinstance(node,data.Return):      raise exception.ReturnException(self.eval(node.value) if node.value else None)
        elif isinstance(node,data.Fn):          self.env.define(node.name,node,'fn',False,'')
        elif isinstance(node,data.Call):
            if node.name=='print':      return self.func_print(node)
            elif node.name=='println':  return self.func_println(node)
            elif node.name=='abs':      return abs(*[self.eval(i) for i in node.args])
            elif node.name=='floor': 
                if not node.args: return self.error(node,"floor() requires exactly 1 argument")
                val=self.eval(node.args[0])
                if not isinstance(val,(int, float)): return self.error(node,"floor() requires a numeric argument")
                return math.floor(val)
            elif node.name=='ceil': 
                if not node.args: return self.error(node,"ceil() requires exactly 1 argument")
                val=self.eval(node.args[0])
                if not isinstance(val,(int, float)): return self.error(node,"ceil() requires a numeric argument")
                return math.ceil(val)
            elif node.name=='round': 
                if not node.args: return self.error(node,"round() requires exactly 1 argument")
                val=self.eval(node.args[0])
                if not isinstance(val,(int, float)): return self.error(node,"round() requires a numeric argument")
                return math.floor(val+0.5)
            fn=self.env.get(node.name)
            if isinstance(fn,data.Fn):
                fnenv=environment.Environment(self.env)
                prev=self.env
                self.env=fnenv
                for param,arg in zip(fn.params,node.args):
                    if param: fnenv.define(param.name,self.eval(arg),param.type_,False,'')
                try:
                    for bod in fn.body: self.eval(bod)
                except exception.ReturnException as e: return e.value
                finally: self.env=prev

    def eval_literal(self,node:data.Literal):
        if '.' in str(node.value): return float(node.value)
        elif node.value.lstrip("-").isdecimal(): return int(node.value)
        elif node.value.startswith('"') or node.value.startswith("'"): return self.eval_string(str(node.value[1:-1]))
        elif node.value=='true': return True
        elif node.value=='false': return False

    def eval_variable(self,node:data.Variable):
        try:
            return self.env.get(node.name)
        except exception.UndefinedVariableException as e:
            self.error(e,f'Undefined variable')
            return None

    def eval_string(self,s:str,args:list|None=None) -> str:
        result=''
        evl,idx=0,0
        while evl<len(s):
            if s[evl]=='{' and evl+1<len(s) and s[evl+1]=='}':
                result+=str(args[idx]) if args and idx < len(args) else '{}'
                idx+=1;evl+=2
            elif s[evl]=='{':
                j=s.index('}',evl)
                result+=str(self.eval(_parser.Parser(_lexer.Lexer(source=s[evl+1:j]).main()).parse_expr_only()))
                evl=j+1
            else:
                result+=s[evl]
                evl+=1
        return result

    def func_print(self,node:data.Call) -> str:
        if len(node.args) > 1:
            t=self.eval(node.args[0])
            g=[self.eval(a) for a in node.args[1:]]
            _=self.eval_string(t,g)
        else:
            _=self.eval(*node.args)
        print(_,end='')
        return _

    def func_println(self,node:data.Call) -> str:
        if len(node.args) > 1:
            t=self.eval(node.args[0])
            g=[self.eval(a) for a in node.args[1:]]
            _=self.eval_string(t,g)
        else:
            _=self.eval(*node.args)
        print(_)
        return _

    def main(self,program:data.Program):
        for stmt in program.statements:
            self.eval(stmt)
