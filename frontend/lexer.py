# SPDX-License-Identifier: MPL-2.0

import data.const as const
import data.data as data
import data.store as store
from util.print import get_async_print


class Lexer:
    def __init__(self,path:str='',source:str='',debug:bool=False):
        if source: self.file:str=source
        else: self.file:str=self.load_file(path)
        self.filelen:int=len(self.file)
        self.current:int=0
        self.current_char:str=self.file[self.current] if self.file else ''
        self.output:list=[]
        self.stack:list=[]
        self.line:int=1
        self.column:int=1
        self.aprint=get_async_print()
        self.debug=debug
        if self.debug: store.debug=not store.debug

    def load_file(self,path:str) -> str:
        with open(path,encoding="utf-8") as f: return f.read()

    def next(self) -> None:
        self.current+=1
        self.column+=1
        if self.current < self.filelen: self.current_char=self.file[self.current]
        
    def get(self,num:int,cfs:bool=False) -> str:
        return self.file[index] if (index:= num if cfs else self.current + num) < self.filelen else ''
    
    def add_token(self, value:str,column:int|None=None,line:int|None=None) -> None:
        if not value: return
        vlen = column if column is not None else self.column - len(value)
        vline = line if line is not None else self.line
        if value in const.RESERVED_WORD:                        self.output.append(data.Token('KEYWORD',value,vline,vlen))
        elif value in const.LINES:                              self.output.append(data.Token('LINE'   ,value,vline,vlen))
        elif value[:2] in const.COMMENT:                        self.output.append(data.Token('COMMENT',value,vline,vlen))
        elif value in const.OPERATORS:                          self.output.append(data.Token('OP'     ,value,vline,vlen))
        elif value in const.END:                                self.output.append(data.Token('END'    ,value,vline,vlen))
        elif value.replace('.', '', 1).isdigit():               self.output.append(data.Token('NUMBER' ,value,vline,vlen))
        elif value.startswith('"') or value.startswith("'"):    self.output.append(data.Token('STRING' ,value,vline,vlen))
        elif value.startswith('f"') or value.startswith("f'"):  value=value[1:];self.output.append(data.Token('FSTRING',value,vline,vlen))
        else:                                                   self.output.append(data.Token('IDENT'  ,value,vline,vlen))

    def main(self):
        while self.current<self.filelen:
            self.stack.append(self.current_char)
            if store.debug:
                self.aprint(self.stack)
            if self.stack[0] in const.SPACES:                       # space
                self.stack.clear()
            elif self.stack[0] in const.LINES:                      # line
                self.add_token("".join(self.stack))
                self.line+=1
                self.column=1
                self.stack.clear()
            elif self.stack[0] in const.END:                        # end
                self.add_token("".join(self.stack))
                self.stack.clear()
            elif self.current_char == '/' and self.get(1) == '/':   # oneline comment
                comment_column = self.column
                self.next()
                while self.current < self.filelen and self.current_char != '\n':
                    self.stack.append(self.current_char)
                    self.next()
                self.add_token("".join(self.stack),comment_column)
                self.add_token('\n',self.column)
                self.line+=1
                self.column=1
                self.stack.clear()
            elif self.current_char == '/' and self.get(1) == '*':   # block comment
                comment_column,comment_line = self.column-1,self.line
                self.next()
                while self.current < self.filelen:
                    self.stack.append(self.current_char)
                    if self.stack[-1] in const.LINES:
                        self.line+=1
                        self.column=1
                    if self.current_char == '*' and self.get(1) == '/':
                        self.next()
                        self.stack.append(self.current_char)
                        break
                    self.next()
                self.add_token(''.join(self.stack),comment_column,comment_line)
                self.stack.clear()
            elif self.current_char in const.ARE:                    # str
                string=self.current_char
                quote=self.current_char
                escape=False
                while True:
                    self.next()
                    if self.current>=self.filelen: break
                    char=self.current_char
                    string+=char
                    self.stack.append(char)
                    if escape: escape=False; continue
                    if char=='\\': escape=True; continue
                    if char==quote: break
                    self.aprint(f'>{string}')
                self.aprint(f'>{string}')
                self.add_token(''.join(self.stack))
                self.stack.clear()
            elif self.stack[0].isdigit():                           # number
                if self.get(1).isdigit() or (self.get(1) == '.' and self.get(2).isdigit() and '.' not in self.stack):
                    pass
                else:
                    self.add_token("".join(self.stack))
                    self.stack.clear()
            elif self.stack[0].isalpha() or self.stack[0] == '_':   # var,reserved word
                if self.get(1) in const.ARE: 
                    self.next()
                    continue
                if self.get(1).isalnum() or self.get(1) == '_':
                    pass
                else:
                    self.add_token("".join(self.stack))
                    self.stack.clear()
            elif self.stack[0] in const.OPERATORS:                  # operator
                if f'{self.stack[0]}{self.get(1)}{self.get(2)}' in const.OPERATORS:
                    self.add_token(f'{self.stack[0]}{self.get(1)}{self.get(2)}')
                    self.stack.clear()
                    self.next()
                    self.next()
                elif f'{self.stack[0]}{self.get(1)}' in const.OPERATORS:
                    self.add_token(f'{self.stack[0]}{self.get(1)}')
                    self.stack.clear()
                    self.next()
                else:
                    self.add_token(self.stack[0])
                    self.stack.clear()
            self.next()
        self.aprint.close()
        if self.debug: store.debug=not store.debug
        return self.output
