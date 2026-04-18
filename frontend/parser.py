import data.const as const
import data.data as data

from typing import Any

Token=data.Token
ErrorFormat=data.ErrorFormat

class Parser:
    def __init__(self,tokens:list[Token]) -> None:
        self.tokens:list[Token]=tokens
        self.current:int=0
        self.current_token:Token=self.get(0)
        self.errors:list=[]
        self.statements:list=[]

    def next(self) -> None:
        print(self.current_token)
        self.current+=1
        if self.current < len(self.tokens):
            self.current_token=self.tokens[self.current]
        else:
            self.current_token=Token('COMMENT',f'SEEING THIS IS AN ERROR! ; NEXT ERROR!',self.current,-1)

    def get(self,num:int,cfs:bool=False) -> Token:
        return self.tokens[num if cfs else self.current + num]

    def error(self,type:str,needed=None) -> None:
        line,col=self.current_token.line,self.current_token.column
        if type=='unknown_keyword':
            self.errors.append(ErrorFormat(type,f'Unknown keyword error:\n{self.current_token}\n',line,col,needed))
        elif type=='expression_isnone':
            self.errors.append(ErrorFormat(type,f'Axpression is None:\n{self.current_token}\n',line,col,needed))
        elif type=='condition_isnone':
            self.errors.append(ErrorFormat(type,f'Condition is None:\n{self.current_token}\n',line,col,needed))
        elif type=='unexpected_type':
            self.errors.append(ErrorFormat(type,f'Unknown type error:\n{self.current_token}\n',line,col,needed))
        elif type=='unexpected_value':
            self.errors.append(ErrorFormat(type,f'Unknown value error:\n{self.current_token}\n',line,col,needed))
        elif type=='unexpected_primary':
            self.errors.append(ErrorFormat(type,f'Unknown primary error:\n{self.current_token}\n',line,col,needed))
        else:
            self.errors.append(ErrorFormat(type,f'Unexpected error:\n{self.current_token}\n',line,col,needed))
        self.skip()

    def skip(self) -> None:
        while self.current < len(self.tokens):
            if self.current_token.type=='END':
                self.next()
                break
            self.next()

    def wskipline(self):
        while self.current_token.type=='LINE': self.next()

    def expect(self,type_:str,value=None) -> data.Token | None:
        if type_==self.current_token.type:
            if value is None or self.current_token.value == value:
                token=self.current_token
                self.next()
                return token
            else:
                self.error('unexpected_value')
                return None    
        else:
            self.error('unexpected_type')
            return None

    # ===== parse =====

    def parse_statement(self):
        if self.current_token.type=='COMMENT':  self.next()
        elif self.current_token.type=='LINE':   self.next()
        elif self.current_token.type=='IDENT':  return self.parse_assign()
        elif self.current_token.type=='KEYWORD':
            if self.current_token.value=='let':     return self.parse_let()
            elif self.current_token.value=='if':    return self.parse_if()
            else: self.error('unknown_keyword')
        else: 
            self.error('unknown_keyword')
            return None

    def parse_primary(self):
        if self.current_token.type=='NUMBER':
            _=self.expect('NUMBER')
            if _: return data.Literal(_.value)
            else: return None
        elif self.current_token.type=='IDENT':
            _=self.expect('IDENT')
            if _: return data.Variable(_.value)
            else: return None
        else: self.error('unknown_primary','NUMBER or IDENT')
        self.next()

    def parse_expression(self) -> data.Expr:
        l=self.parse_term()
        while self.current_token.value in const.EXPRS:
            o=self.current_token.value
            self.next()
            r=self.parse_term()
            l=data.Binary(l,o,r)
        return data.Expr([l])

    def parse_term(self):
        l=self.parse_power()
        while self.current_token.value in const.TERMS:
            o=self.current_token.value
            self.next()
            r=self.parse_power()
            l=data.Binary(l,o,r)
        return l

    def parse_power(self):
        l = self.parse_primary()
        if self.current_token.value in const.POWER:
            o = self.current_token.value
            self.next()
            r = self.parse_power()
            return data.Binary(l, o, r)
        return l

    def parse_assign(self):
        idn=self.expect('IDENT')
        self.expect('OP','=')
        exp=self.parse_expression()
        self.expect('END')
        if idn: 
            return data.Assign(str(idn.value),exp)
        else:
            self.error('expression_isnone')
            return None

    def parse_block(self):
        blocks=[]
        while True:
            tm=self.parse_statement()
            if tm: blocks.append(tm)
            if self.current_token.type=='OP' and self.current_token.value=='}': break
            if self.current >= len(self.tokens): break
        return blocks

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

    def parse_if(self):
        self.expect('KEYWORD','if')
        self.expect('OP','('); self.wskipline()
        if self.current_token.value!=')': con=self.parse_expression()
        else: self.error('condition_isnone')
        self.wskipline()
        self.expect('OP',')'); self.wskipline()
        self.expect('OP','{'); self.wskipline()
        bod=self.parse_block()
        self.expect('OP','}'); self.wskipline()
        if self.current_token.type=='END':
            self.next()
            return data.If(con,bod,None)
        
        return data.If(con,bod,None)

    # ===== END =====

    def main(self) -> tuple[data.Program, list[Any]]:
        statements=[]
        while self.current < len(self.tokens):
            stmt=self.parse_statement()
            if stmt: statements.append(stmt)
        return data.Program(statements),self.errors
