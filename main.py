import core.filepath as _file
import frontend.lexer as _lexer
import frontend.parser as _parser
import data.const as const
import data.store as store

N=25

def FileInitialization():
    setting=_file.loader()
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
    if store.debug: print(f'\n{parsed}')

if __name__=="__main__":
    if store.debug: print('start initialization...')
    FileInitialization()
    if store.debug:
        print(f'{'='*N}file{'='*N}')
        with open(const.FILEPATH) as f: print(f.read())
        print(f'{'='*(N*2+4)}')
        print('Starting frontend...')
    tokens=run_Lexer()
    run_Parser(tokens)
