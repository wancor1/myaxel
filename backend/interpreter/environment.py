# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations
import data.exception as exception
class Environment:
    def __init__(self,parent:Environment|None=None) -> None:
        self.parent=parent
        self.variable:dict[str,dict[str,object]]={}

    def define(self,name:str,value,vtype:str,mut:bool,of:str) -> None:
        if not name in self.variable: self.variable[name]={'value': value,'type': vtype,'mut':mut,'overflow':of}

    def get(self,name:str) -> object | None:
        if name in self.variable: return self.variable[name]['value']
        if self.parent:
            return self.parent.get(name)
        raise exception.UndefinedVariableException(name)

    def set(self,name,value):
        if name in self.variable: self.variable[name]['value']=value
        if self.parent:
            return self.parent.set(name,value)
        return None

if __name__=='__main__':
    env=Environment()
    env.define('a',1,'int',False,'wrap')
    print(env.get('a'))
    env.define('b',2,'int',True,'wrap')
    env.set('b',2)
    print(env.get('b'))
    print(env.variable)
