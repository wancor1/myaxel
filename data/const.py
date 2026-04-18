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
    '.',':'
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
    'int4','int8','int16','int32','int64','int128','int256',
    'uint4','uint8','uint16','uint32','uint64','uint128','uint256',
    'float4','float8','float16','float32','float64','float128','float256',
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
