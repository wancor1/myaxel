# SPDX-License-Identifier: MPL-2.0

import core.initialization as _initialization
import frontend.lexer as _lexer
import frontend.parser as _parser
import resolver.resolver as _resolver
import backend.interpreter.interpreter as _interpreter
import data.const as const
import data.store as store

N=25

def Initialization():
    setting=_initialization.Initialization()
    setting.main()
    store.fromlexer=True

def run_Lexer():
    if store.debug: print(f'\n{'='*N}Lexer output{'='*N}')
    lexer=_lexer.Lexer(const.FILEPATH)
    token=lexer.main()
    if store.debug: print(f'\n{token}')
    return token

def run_Parser(token):
    if store.debug: print(f'\n{'='*N}Parser output{'='*N}')
    parser=_parser.Parser(token)
    parsed=parser.main()
    if store.debug: 
        print(f'\n{parsed}')
        if parsed[1]:
            print(f'\n{'='*int(N/2)}ERROR{'='*int(N/2)}')
            for i,l in enumerate(parsed[1], start=1): print(f'[{i}]\n{l.text}',end='\n'*2)
            print(f'{'='*(N+5)}')
    return parsed

def run_Resolver(program):
    if store.debug: print(f'\n{'='*N}Resolver output{'='*N}')
    resolver=_resolver.Resolver(program[0])
    resolved=resolver.main()
    if store.debug: 
        print(f'\nError:{resolved}')
        if resolved:
            print(f'\n{'='*int(N/2)}ERROR{'='*int(N/2)}')
            for i,l in enumerate(resolved, start=1): print(f'[{i}]\n{l.text}',end='\n'*2)
            print(f'{'='*(N+5)}')
    return resolved

def run_Interpreter(program):
    store.fromlexer=False
    if store.debug: print(f'\n{'='*N}Interpreter output{'='*N}')
    interpreter=_interpreter.Interpreter()
    mon=interpreter.main(program)
    if store.debug: print(f'\n{'='*N}{'='*len('Interpreter output')}{'='*N}')
    return mon

if __name__=="__main__":
    if store.debug: print('start initialization...')
    Initialization()
    if store.debug:
        print(f'{'='*N}file{'='*N}')
        with open(const.FILEPATH,encoding="utf-8") as f: print(f.read())
        print(f'{'='*(N*2+4)}')
        print('Starting frontend...')
    tokens=run_Lexer()
    parsed=run_Parser(tokens)
    if not parsed[1]: resolved=run_Resolver(parsed)
    else: exit(1)
    if not resolved: run_Interpreter(parsed[0])
    else: exit(1)
