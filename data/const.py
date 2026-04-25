import os

EXT=".myx"

FILENAME='test.myx'
DIRPATH=os.path.dirname(os.path.abspath(__file__))
FILEPATH=os.path.join(DIRPATH,FILENAME)

SPACES=[' ', '\t']
LINES=['\n']
ARE=['"',"'"]
END=[';']
CALCULATIONS=[
    '+','-','*','/','**'
    '(',')'
]
EXPRS=[
    '+','-'
]
TERMS=[
    '*','/'
]
POWER=[
    '**'
]
OVERFLOWMODE=[
    'panic','wrap','sat'
]
OPERATORS=[
    '+','-','*','/','**','=',
    '(',')','{','}','"',"'",
    '<','>','==','!=','===',
    '.',':',','
]
RESERVED_WORD=[
    'let','mut','panic','wrap','sat',
    'if','else','elif',
    'fn',
    'while','for',
    'return','break','continue',
    'import','use',
    'pass',
    'int','uint','float','str','bool','null'
    'i4','i8','i6','i32','i64','i128','i256',
    'u4','u8','u6','u32','u64','u128','u256',
    'f8','f16','f32','f64','f128','f256',
]
COMMENT=[
    '//','/*','*/'
]

TYPE=['int','uint','float','str','bool','null']


# =====

KEYWORD_MAP = {
    'let':'LET', 'fn':'FN', 'mut':'MUT',
    'if':'IF', 'else':'ELSE', 'elif':'ELIF',
    'while':'WHILE', 'for':'FOR', 'return':'RETURN',
    'break':'BREAK', 'continue':'CONTINUE', 'pass':'PASS',
    'import':'IMPORT', 'use':'USE',
}
OP_MAP = {
    '+':'PLUS', '-':'MINUS', '*':'ASTARISK',
    '/':'SLASH', '=':'EQUAL',
}
