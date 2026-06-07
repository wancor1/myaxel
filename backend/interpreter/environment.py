# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations
import data.exception as exception
class Environment:
    def __init__(self,parent:Environment|None=None) -> None:
        self.parent=parent
        self.variable:dict[str,dict[str,object]]={}

    def _list(self):
        return self.variable

    def define(self,name:str,value,vtype:str,mut:bool,of:str) -> None:
        self.variable[name]={'value': value,'type': vtype,'mut':mut,'overflow':of}

    def get(self,name:str,key:str='value') -> object:
        if name in self.variable:
            if key and key in self.variable[name]: return self.variable[name][key]
            elif not key: return self.variable[name]
            else: raise exception.UnknownVariableKeyException(key)
        if self.parent: return self.parent.get(name,key)
        raise exception.UndefinedVariableException(name)

    def set(self,name,value):
        if name in self.variable: self.variable[name]['value']=value
        elif self.parent: return self.parent.set(name,value)
