# SPDX-License-Identifier: MPL-2.0

import data.const as const
import data.store as store
import data.data as data
import util.util as util

class Parser:
    def __init__(self,tokens:list[data.Token],debug:bool=False) -> None:
        self.tokens:list[data.Token]=tokens
        self.current:int=0
        self.current_token:data.Token=self.get(0)
        self.current_token_tv=self.current_token.type,self.current_token.value
        self.errors:list=[]
        self.statements:list=[]
        self.blocker:int=0
        self.for_counter:int=0
        self.debug=debug
        if self.debug: store.debug=not store.debug

    def next(self,c:int=1) -> None:
        for i in range(c):
            if store.debug and store.fromlexer: print(self.current_token)
            self.current+=1
            if self.current < len(self.tokens):
                self.current_token=self.tokens[self.current]
                self.current_token_tv=self.current_token.type,self.current_token.value
                self.blocker=0
            else:
                self.blocker+=1
                self.current_token=data.Token('ERROR',f'SEEING THIS IS AN ERROR! ; NEXT ERROR!',self.current,-1)
                if self.blocker>=20: raise type("LoopError", (Exception,), {})("Unknown Error:heart:")

    def get(self,num:int=1,cfs:bool=False) -> data.Token:
        i=num if cfs else self.current+num
        if 0<=i<len(self.tokens): return self.tokens[i]
        return data.Token('ERROR',f'SEEING THIS IS AN ERROR! ; GET INDEX ERROR!',self.current,-1)

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
        elif type=='is_not_op':
            self.errors.append(data.ErrorFormat(type,f'It is not operation:\n  {self.current_token}',line,col,needed))
        elif type=='is_not_compound':
            self.errors.append(data.ErrorFormat(type,f'It is not compound:\n  {self.current_token}',line,col,needed))
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
            self.next()

    def wskipline(self) -> None:
        while self.current_token.type=='LINE':
            self.next()

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

    def parse_statement(self) -> object:
        if self.current_token.type=='COMMENT':  self.next()
        elif self.current_token.type=='ERROR':  self.next()
        elif self.current_token.type=='LINE':   self.next()
        elif self.current_token.type=='IDENT':
            if  (_:=self.get().value) in const.IDC:     return self.parse_crement()
            elif _=='(':                                return self.parse_funccall()
            elif _=='.':
                a=self.parse_postfix()
                self.expect('END')
                return a
            elif _ in const.COMPOUND:                   return self.parse_compoundassign()
            else:                                       return self.parse_assign()
        elif self.current_token.type=='KEYWORD':
            if self.current_token.value=='let':         return self.parse_let()
            elif self.current_token.value=='if':        return self.parse_if()
            elif self.current_token.value=='fn':        return self.parse_fn()
            elif self.current_token.value=='while':     return self.parse_while()
            elif self.current_token.value=='for':       return self.parse_for()
            elif self.current_token.value=='return':    return self.parse_return()
            elif self.current_token.value=='break':     return self.parse_break()
            elif self.current_token.value=='continue':  return self.parse_continue()
            elif self.current_token.value=='import':    return self.parse_import()
            elif self.current_token.value=='use':       return self.parse_use()
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
        l=self.parse_postfix()
        if self.current_token.value in const.POWER:
            o=self.current_token.value
            self.next()
            r=self.parse_power()
            return data.Binary(l,o,r)
        return l

    def parse_primary(self) -> data.x:
        if self.current_token_tv==('OP','-'):  self.next(); return data.Unary('-', self.parse_primary())
        elif self.current_token.type=='NUMBER':             return data.Literal(self.expect('NUMBER').value)
        elif self.current_token.type=='IDENT':              return self.parse_primary_ident()
        elif self.current_token.type=='STRING':             return data.Literal(self.expect('STRING').value)
        elif self.current_token.type=='FSTRING':            return data.Literal(self.expect('FSTRING').value,True)
        elif self.current_token.value in ('true','false'):  return data.Literal(self.expect('KEYWORD').value)
        elif self.current_token_tv==('OP','['):             return self.parse_primary_list()
        elif self.current_token_tv==('OP','('):             return self.parse_paren()
        else: self.error('unknown_primary','NUMBER | IDENT | STRING')
        self.next()
        return data.Literal('')

    def parse_paren(self):
        self.expect('OP','(')
        self.wskipline()
        first=self.parse_expression()
        if self.current_token_tv==('OP',','):
            return self.parse_primary_tuple(first)
        else:
            return self.parse_grouping(first)

    def parse_primary_tuple(self,first):
        ls:list=[]
        self.expect('OP',',')
        while self.current_token_tv!=('OP',')'):
            ls.append(self.parse_expression())
            if self.current_token_tv==('OP',','): self.next()
        self.expect('OP',')')
        return data.Tuple([first]+ls)

    def parse_grouping(self,first):
        self.expect('OP',')')
        return first.value[0]

    def parse_primary_ident(self) -> data.Call | data.Access | data.MethodCall | data.Variable:
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

    def parse_primary_list(self) -> data.Array:
        value:list=[]
        self.expect('OP','[')
        while self.current_token_tv!=('OP',']'):
            value.append(self.parse_expression())
            if self.current_token_tv==('OP',','): self.expect('OP',',')
        self.expect('OP',']')
        return data.Array(value)

    def parse_postfix(self):
        e=self.parse_primary()
        while self.current_token_tv in(('OP','['),('OP','.')):
            if self.current_token_tv==('OP','['):
                self.expect('OP','[')
                i=self.parse_expression()
                self.expect('OP',']')
                e=data.Index(e,i)
            else:
                self.expect('OP','.')
                if self.current_token.type=='NUMBER':
                    n=self.expect('NUMBER').value
                    e=data.TupleAccess(e,int(n))
                elif self.current_token.type=='IDENT':
                    m=self.expect('IDENT')
                    if self.current_token_tv==('OP','('):
                        self.expect('OP','(')
                        a:list[data.Expr|tuple]=[]
                        while self.current_token_tv!=('OP',')'):
                            self.wskipline()
                            if self.get().value=='=':
                                n=self.current_token.value
                                self.next(2)
                                a.append((n,self.parse_expression()))
                            else: a.append(self.parse_expression())
                            self.wskipline()
                            if self.current_token_tv==('OP',','): self.next()
                            self.wskipline()
                        self.expect('OP',')')
                        e=data.MethodCall(e,m.value,a)
                    else:
                        e=data.Access(e,m.value)
        return e

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

    def parse_compoundassign(self) -> data.CompoundAssign:
        idn=self.expect('IDENT')
        if self.current_token.type=='OP':
            if self.current_token.value in const.COMPOUND:
                _op=self.current_token.value
                self.next()
            else: self.error('is_not_compound'); return data.CompoundAssign('',data.Expr([]),'')
        else: self.error('is_not_op'); return data.CompoundAssign('',data.Expr([]),'')
        exp=self.parse_expression()
        self.expect('END')
        if idn: return data.CompoundAssign(str(idn.value),exp,_op)
        else:
            self.error('expression_isnone')
            return data.CompoundAssign('',data.Expr([]),'')

    def parse_assignexpr(self) -> data.Assign:
        idn=self.expect('IDENT')
        if self.current_token.type=='OP':
            if self.current_token.value in const.OPERATORS:
                _op=self.current_token.value
                self.next()
        exp=self.parse_expression()
        if idn: return data.Assign(str(idn.value),exp)
        else:
            self.error('expression_isnone')
            return data.Assign('',data.Expr([]))

    def parse_block(self,stop:tuple=('OP','}')) -> list:
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
        _=self.parse_expression()
        if self.debug: store.debug=not store.debug
        return _

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
        els:list=[]
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
            return data.If(con,ifbod,[])
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
            self.wskipline()
            self.expect('OP','}')
        if self.current_token.type=='END':
            self.next()
            for elcon,elifbod in reversed(elifs):
                els=[data.If(elcon,elifbod,[els])]
        return data.If(con,ifbod,els)

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
            _ident=self.expect('IDENT').value
            self.expect('KEYWORD','in')
            _start=self.parse_expression()
            if self.current_token_tv==('OP','..'):
                self.expect('OP','..')
                _end=self.parse_expression().value[0]
                self.wskipline()
                _cond=data.Expr([data.Binary(data.Variable(str(_ident)),'<',_end)])
                _upda=util.increment(str(_ident))
                self.expect('OP','{')
                _body=self.parse_block()
                self.expect('OP','}')
                self.expect('END')
                return [util.let(str(_ident),_start,True),data.While(_cond,_body+[_upda])]
            else:
                self.for_counter+=1
                self.wskipline()
                _in=f'__for_idx_{self.for_counter}__'
                _cond=data.Expr([data.Binary(data.Variable(_in),'<',data.Call('len',[_start]))])
                _upda=util.increment(_in)
                self.expect('OP','{')
                _body=self.parse_block()
                self.expect('OP','}')
                self.expect('END')
                _=util.let(str(_ident),data.Expr([data.Index(_start.value[0],data.Expr([data.Variable(_in)]))]))
                return [util.let(_in,data.Expr([data.Literal('0')]),True),data.While(_cond,[_]+_body+[_upda])]
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

    def parse_import(self) -> data.Import:
        self.expect('KEYWORD','import')
        path=self.expect('IDENT').value
        self.expect('END')
        return data.Import(path)

    def parse_use(self):
        self.expect('KEYWORD','use')
        m=self.expect('IDENT').value
        self.expect('OP','.')
        n=self.expect('IDENT').value
        self.expect('END')
        return data.Use(m,n)

    # ===== END =====

    def main(self) -> tuple[data.Program, list]:
        statements=[]
        while self.current < len(self.tokens):
            stmt=self.parse_statement()
            if isinstance(stmt,list): statements.extend(stmt)
            elif stmt: statements.append(stmt)
            if self.debug: store.debug=not store.debug
        return data.Program(statements),self.errors
