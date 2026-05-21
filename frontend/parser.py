# SPDX-License-Identifier: MPL-2.0

import data.const as const
import data.store as store
import data.data as data
import util.util as util

from typing import Any

class Parser:
    def __init__(self,tokens:list[data.Token]) -> None:
        self.tokens:list[data.Token]=tokens
        self.current:int=0
        self.current_token:data.Token=self.get(0)
        self.current_token_tv=self.current_token.type,self.current_token.value
        self.errors:list=[]
        self.statements:list=[]
        self.blocker:int=0

    def next(self,c:int=1) -> bool:
        for i in range(c):
            if store.debug: print(self.current_token)
            self.current+=1
            if self.current < len(self.tokens):
                self.blocker=0
                self.current_token=self.tokens[self.current]
                self.current_token_tv=self.current_token.type,self.current_token.value
            else:
                self.blocker+=1
                self.current_token=data.Token('ERROR',f'SEEING THIS IS AN ERROR! ; NEXT ERROR!',self.current,self.blocker)
                if self.blocker>=50: return True
        return False

    def get(self,num:int=1,cfs:bool=False) -> data.Token:
        try:
            return self.tokens[num if cfs else self.current + num]
        except:
            return data.Token('ERROR',f'SEEING THIS IS AN ERROR! ; GET ERROR!',self.current,-1)

    def error(self,type:str,needed=None) -> None:
        line,col=self.current_token.line,self.current_token.column
        if type=='unknown_keyword':
            self.errors.append(data.ErrorFormat(type,f'Unknown keyword error:\n  {self.current_token}',line,col,needed))
        elif type=='invalid_syntax_for':
            self.errors.append(data.ErrorFormat(type,f'invalid for loop syntax:\n  {self.current_token}',line,col,needed))
        elif type=='wrong_for_ident':
            self.errors.append(data.ErrorFormat(type,f'error for loop ident:\n  {self.current_token}',line,col,needed))
        elif type=='expression_isnone':
            self.errors.append(data.ErrorFormat(type,f'Expression is None:\n  {self.current_token}',line,col,needed))
        elif type=='condition_isnone':
            self.errors.append(data.ErrorFormat(type,f'Condition is None:\n  {self.current_token}',line,col,needed))
        elif type=='unexpected_type':
            self.errors.append(data.ErrorFormat(type,f'Unknown type error:\n  {self.current_token}',line,col,needed))
        elif type=='unexpected_value':
            self.errors.append(data.ErrorFormat(type,f'Unknown value error:\n  {self.current_token}',line,col,needed))
        elif type=='unexpected_primary':
            self.errors.append(data.ErrorFormat(type,f'Unknown primary error:\n  {self.current_token}',line,col,needed))
        elif type=='not_crement':
            self.errors.append(data.ErrorFormat(type,f'It is not in/decrement:\n  {self.current_token}',line,col,needed))
        elif type=='forgot_end':
            self.errors.append(data.ErrorFormat(type,f'Maybe you forgot the end:\n  {self.current_token}',line,col,needed))
        elif type=='howd_it_get_here':
            self.errors.append(data.ErrorFormat(type,f'How did it get to this point in the process?\n  {self.current_token}',line,col,needed))
        elif type=='wrong_pos_end':
            self.errors.append(data.ErrorFormat(type,f'end...??\n  {self.current_token}',line,col,needed))
        elif type=='dontcry':
            self.errors.append(data.ErrorFormat(type,f'Don\'t cry, it\'s okay.\n  {self.current_token}',line,col,needed))
        else:
            self.errors.append(data.ErrorFormat(type,f'Unexpected error:\n  {self.current_token}',line,col,needed))
        self.skip()

    def skip(self) -> None:
        while self.current < len(self.tokens):
            if self.current_token.type=='END':
                self.next()
                break
            if self.next(): break

    def wskipline(self) -> None:
        while self.current_token.type=='LINE':
            if self.next(): break

    def expect(self,type_:str,value:str|None=None) -> data.Token:
        if type_==self.current_token.type:
            if value is None or self.current_token.value == value:
                token=self.current_token
                self.next()
                return token
            else:
                self.error('unexpected_value')
                return data.Token('ERROR','unexpected_value',-1,-1)
        else:
            if type_=='END':
                self.error('forgot_end')
                return data.Token('ERROR','forgot_end',-1,-1)
            self.error('unexpected_type')
            return data.Token('ERROR','unexpected_type',-1,-1)

    # ===== parse =====

    def parse_statement(self) -> Any:
        if self.blocker>=50: return 
        if self.current_token.type=='COMMENT':  self.next()
        elif self.current_token.type=='ERROR':  self.next()
        elif self.current_token.type=='LINE':   self.next()
        elif self.current_token.type=='IDENT':
            if self.get().value in const.IDC:   return self.parse_crement()
            if self.get().value=='(':           return self.parse_funccall()
            else:                               return self.parse_assign()
        elif self.current_token.type=='KEYWORD':
            if self.current_token.value=='let':         return self.parse_let()
            elif self.current_token.value=='if':        return self.parse_if()
            elif self.current_token.value=='fn':        return self.parse_fn()
            elif self.current_token.value=='while':     return self.parse_while()
            elif self.current_token.value=='for':       return self.parse_for()
            elif self.current_token.value=='return':    return self.parse_return()
            elif self.current_token.value=='break':     return self.parse_break()
            elif self.current_token.value=='continue':  return self.parse_continue()
            else: self.error('unknown_keyword')
        elif self.current_token.type=='END':
            if self.get().type=='END':
                self.next()
                self.error('dontcry')
            else: self.error('wrong_pos_end')
        else:
            self.error('unknown_keyword')
            return None

    def parse_crement(self,flag=True):
        ident=self.current_token.value
        self.next()
        op=self.current_token.value
        self.next()
        if flag: self.expect('END')
        if op=='++':    return util.increment(ident)
        elif op=='--':  return util.decrement(ident)
        else:           return self.error('not_crement')

    def parse_expression(self) -> data.Expr:
        l=self.parse_comp()
        while self.current_token.value in const.EXPRS:
            o=self.current_token.value
            self.next()
            r=self.parse_comp()
            l=data.Binary(l,o,r)
        return data.Expr([l])

    def parse_comp(self):
        l=self.parse_equality()
        while self.current_token.value in const.COMPARISON:
            o=self.current_token.value
            self.next()
            r=self.parse_equality()
            l=data.Binary(l,o,r)
        return l

    def parse_equality(self):
        l=self.parse_term()
        while self.current_token.value in const.EQUALITY:
            o=self.current_token.value
            self.next()
            r=self.parse_term()
            l=data.Binary(l,o,r)
        return l

    def parse_term(self):
        l=self.parse_power()
        while self.current_token.value in const.TERMS:
            o=self.current_token.value
            self.next()
            r=self.parse_power()
            l=data.Binary(l,o,r)
        return l

    def parse_power(self):
        l=self.parse_primary()
        if self.current_token.value in const.POWER:
            o=self.current_token.value
            self.next()
            r=self.parse_power()
            return data.Binary(l,o,r)
        return l

    def parse_primary(self) -> data.Literal | data.Variable | data.Call | data.Unary:
        if self.current_token.type == 'OP' and self.current_token.value == '-':
            self.next()
            return data.Unary('-', self.parse_primary())
        elif self.current_token.type=='NUMBER':
            _=self.expect('NUMBER')
            if _: return data.Literal(_.value)
            else: return data.Literal('')
        elif self.current_token.type=='IDENT':
            if self.get().value=='(':
                _=self.expect('IDENT')
                self.expect('OP','(')
                self.wskipline()
                args:list[data.Expr|tuple]=[]
                while self.current_token_tv!=('OP',')'):
                    self.wskipline()
                    if self.get().value=='=':
                        name=self.current_token.value
                        self.next(2)
                        args.append((name,self.parse_expression()))
                    else: args.append(self.parse_expression())
                    self.wskipline()
                    if self.current_token_tv==('OP',','): self.next()
                    self.wskipline()
                self.wskipline()
                self.expect('OP',')')
                return data.Call(_.value,args)
            else:
                _=self.expect('IDENT')
                if _: return data.Variable(_.value)
                else: return data.Variable('')
        elif self.current_token.type == 'STRING':
            _ = self.expect('STRING')
            return data.Literal(_.value)
        elif self.current_token.value in ('true','false'): return data.Literal(self.expect('KEYWORD').value)
        else: self.error('unknown_primary','NUMBER | IDENT | STRING')
        if self.next(): return data.Literal('')
        return data.Literal('')

    def parse_assign(self) -> data.Assign:
        idn=self.expect('IDENT')
        self.expect('OP','=')
        exp=self.parse_expression()
        self.expect('END')
        if idn:
            return data.Assign(str(idn.value),exp)
        else:
            self.error('expression_isnone')
            return data.Assign('',data.Expr([]))

    def parse_assignexpr(self) -> data.Assign:
        idn=self.expect('IDENT')
        if self.current_token.type=='OP':
            if self.current_token.value in const.OPERATORS:
                _op=self.current_token.value
                self.next()
        exp=self.parse_expression()
        if idn:
            return data.Assign(str(idn.value),exp)
        else:
            self.error('expression_isnone')
            return data.Assign('',data.Expr([]))

    def parse_block(self,stop:tuple=('OP','}')) -> list[Any]:
        blocks:list=[]
        while True:
            tm=self.parse_statement()
            if tm: blocks.append(tm)
            if self.current_token_tv==stop: break
            if self.current >= len(self.tokens): break
        return blocks

    def parse_params(self) -> list[data.Parm]:
        p=[]
        while self.current_token_tv!=('OP',')'):
            name,type_=None,''
            name=str(self.current_token.value)
            self.next()
            if self.current_token_tv==('OP',':'):
                self.expect('OP',':')
                type_=str(self.current_token.value)
                self.next();self.wskipline()
            p.append(data.Parm(name,type_))
            if self.current_token_tv==('OP',','): self.expect('OP',',')
        return p

    def parse_expr_only(self) -> data.Expr:
        return self.parse_expression()

    # === blocks ===

    def parse_return(self) -> data.Return:
        if self.current_token_tv==('KEYWORD','return'):
            self.expect('KEYWORD','return')
            if self.current_token.type=='END':
                self.expect('END')
                return data.Return(None)
            else:
                _=self.parse_expression()
                self.expect('END')
                return data.Return(_)
        self.error('howd_it_get_here')
        return data.Return(data.Expr([]))

    def parse_break(self):
        self.expect('KEYWORD','break')
        self.expect('END')
        return data.Break()

    def parse_continue(self):
        self.expect('KEYWORD','continue')
        self.expect('END')
        return data.Continue()

    def parse_let(self) -> data.Let | None:
        mut,ofm,num=False,'wrap',None
        tpe:str='Null'
        self.expect('KEYWORD','let')
        if self.current_token.type=='IDENT':
            ide=self.expect('IDENT')
        else:
            mut=self.expect('KEYWORD','mut')
            if self.current_token.type=='KEYWORD' and self.current_token.value in const.OVERFLOWMODE:
                ofm=self.current_token.value
                self.next()
                ide=self.expect('IDENT')
            else:
                ide=self.expect('IDENT')
        if self.current_token.type=='OP':
            if self.current_token.value==':':
                self.expect('OP',':')
                tpe=str(self.current_token.value)
                self.next()
            if self.current_token.value=='=':
                self.expect('OP','=')
                num=self.parse_expression()
        self.expect('END')
        if ide: return data.Let(str(ide.value),num,bool(mut),ofm,tpe)
        else: return None

    def parse_if(self) -> data.If:
        elifs=[]
        els=None
        con=data.Expr([])
        elcon=data.Expr([])
        self.expect('KEYWORD','if')
        self.expect('OP','('); self.wskipline()
        if self.current_token.value!=')': con=self.parse_expression()
        else: self.error('condition_isnone')
        self.wskipline()
        self.expect('OP',')'); self.wskipline()
        self.expect('OP','{'); self.wskipline()
        if self.current_token_tv!=('OP','}'): ifbod=self.parse_block()
        else: ifbod=[]
        self.expect('OP','}'); self.wskipline()
        if self.current_token.type=='END':
            self.next()
            return data.If(con,ifbod,None)
        while self.current_token_tv==('KEYWORD','elif'):
            self.expect('KEYWORD','elif')
            self.expect('OP','('); self.wskipline()
            if self.current_token.value!=')': elcon=self.parse_expression()
            else: self.error('condition_isnone')
            self.wskipline()
            self.expect('OP',')'); self.wskipline()
            self.expect('OP','{'); self.wskipline()
            elifbod=self.parse_block()
            self.expect('OP','}'); self.wskipline()
            elifs.append((elcon,elifbod))
        if self.current_token_tv==('KEYWORD','else'):
            self.expect('KEYWORD','else')
            self.expect('OP','{')
            els=self.parse_block()
            self.expect('OP','}')
        if self.current_token.type=='END':
            self.next()
            for elcon,elifbod in reversed(elifs):
                els=data.If(elcon,elifbod,[els])
        return data.If(con,ifbod,[els])

    def parse_fn(self) -> data.Fn:
        retp=None
        self.expect('KEYWORD','fn')
        name=self.current_token.value
        self.next()
        self.expect('OP','(');self.wskipline()
        params=self.parse_params()
        self.expect('OP',')')
        if self.current_token_tv==('OP',':'):
            self.expect('OP',':')
            retp=str(self.current_token.value)
            self.next()
        self.wskipline()
        self.expect('OP','{');self.wskipline()
        bod=self.parse_block()
        self.expect('OP','}');self.wskipline()
        self.expect('END')
        return data.Fn(str(name),params,retp,bod)

    def parse_while(self) -> data.While:
        con=data.Expr([])
        self.expect('KEYWORD','while')
        self.expect('OP','('); self.wskipline()
        if self.current_token.value!=')': con=self.parse_expression()
        else: self.error('condition_isnone')
        self.wskipline()
        self.expect('OP',')'); self.wskipline()
        self.expect('OP','{'); self.wskipline()
        bod=self.parse_block()
        self.expect('OP','}')
        self.expect('END')
        return data.While(con,bod)

    def parse_for(self) -> list:
        _valu=data.Assign('',data.Expr([]))
        _cond=data.Expr([])
        _upda=data.Assign('',data.Expr([]))
        self.expect('KEYWORD','for')
        if self.current_token_tv==('OP','('):
            self.expect('OP','('); self.wskipline()
            if self.current_token.value!=')':
                _valu=self.parse_assignexpr()
                if not _valu: _valu=data.Assign('',data.Expr([]))
                self.expect('OP',',');self.wskipline()
                _cond=self.parse_expression()
                self.expect('OP',',');self.wskipline()
                _upda=self.parse_crement(flag=False)
                self.wskipline()
                self.expect('OP',')')
                self.wskipline()
            else: self.error('condition_isnone')
            self.expect('OP','{'); self.wskipline()
            _body=self.parse_block()
            self.expect('OP','}')
            self.expect('END')
            return [util.let(str(_valu.name),_valu.value.value[0].value,True),data.While(_cond,_body+[_upda])]
        elif self.current_token.type=='IDENT':
            _ident=self.expect('IDENT')
            if _ident: _ident=_ident.value
            else: self.error('wrong_for_ident')
            self.expect('KEYWORD','in')
            _start=str(self.current_token.value)
            self.next()
            self.expect('OP','..')
            _end=str(self.current_token.value)
            self.next()
            self.wskipline()
            _cond=data.Expr([data.Binary(data.Variable(str(_ident)),'<',data.Literal(_end))])
            _upda=util.increment(str(_ident))
            self.expect('OP','{')
            _body=self.parse_block()
            self.expect('OP','}')
            self.expect('END')
            return [util.let(str(_ident),_start,True),data.While(_cond,_body+[_upda])]
        else: self.error('invalid_syntax_for')
        return []

    def parse_funccall(self) -> data.Call:
        n=self.expect('IDENT').value
        self.expect('OP','(')
        self.wskipline()
        args:list[data.Expr|tuple]=[]
        while self.current_token_tv!=('OP',')'):
            self.wskipline()
            if self.get().value=='=':
                name=self.current_token.value
                self.next(2)
                args.append((name,self.parse_expression()))
            else: args.append(self.parse_expression())
            self.wskipline()
            if self.current_token_tv==('OP',','): self.next()
            self.wskipline()
        self.wskipline()
        self.expect('OP',')');self.expect('END')
        return data.Call(n,args)

    # ===== END =====

    def main(self) -> tuple[data.Program, list[Any]]:
        statements=[]
        while self.current < len(self.tokens):
            stmt=self.parse_statement()
            if isinstance(stmt,list): statements.extend(stmt)
            elif stmt: statements.append(stmt)
        return data.Program(statements),self.errors
