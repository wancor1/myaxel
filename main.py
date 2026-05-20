import core.initialization   as _initialization
import frontend.lexer as _lexer
import frontend.parser as _parser
import backend.interpreter.interpreter as _interpreter
import data.const as const
import data.store as store

N=25

def Initialization():
    setting=_initialization.Initialization()
    setting.main()

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
            for i,l in enumerate(parsed[1], start=1):
                print(f'[{i}]\n{l.text}',end='\n'*2)
            print(f'{'='*(N+5)}')
    return parsed

def run_Interpreter(program):
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
        with open(const.FILEPATH) as f: print(f.read())
        print(f'{'='*(N*2+4)}')
        print('Starting frontend...')
    tokens=run_Lexer()
    parsed=run_Parser(tokens)
    if not parsed[1]:
        run_Interpreter(parsed[0])
