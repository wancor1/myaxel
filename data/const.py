# SPDX-License-Identifier: MPL-2.0

import os

EXT=".myx"

FILENAME='test.myx'
DIRPATH=os.path.dirname(os.path.abspath(__file__))
FILEPATH=os.path.join(DIRPATH,FILENAME)

SPACES={' ', '\t'}
LINES={'\n'}
ARE={'"',"'"}
END={';'}
CALCULATIONS={
    '+','-','*','/','**','%',
    '(',')',
    '<<','>>','|','&','^'
}
COMPOUND={
    '+=','-=','*=','/='
}
EXPRS={
    '+','-','&&','||','<<','>>','|','&','^'
}
TERMS={
    '*','/','%'
}
POWER={
    '**'
}
IDC={
    '++','--'
}
PRIMARY={
    '..'
}
COMPARISON={
    '<','>','<=','>='
}
EQUALITY={
    '==','===','!='
}
OVERFLOWMODE={
    'panic','wrap','sat'
}
OPERATORS={
    '+','-','*','/','**','%',
    '=','+=','-=','*=','/=',
    '(',')','{','}','[',']','"',"'",
    '<','>','<=','>=','==','!=','===',
    '.',':',',','..',
    '&&','||',
    '^','~','<<','>>','&','|',
    '++','--',
    '{','}'
}
RESERVED_WORD={
    'let','mut','panic','wrap','sat',
    'if','else','elif',
    'fn',
    'while','for',
    'return','break','continue',
    'import','use',
    'pass',
    'in','as',
    'true','false',
    'any','int','uint','float','str','bool','null',
    'i4','i8','i16','i32','i64','i128','i256','i1024',
    'u4','u8','u16','u32','u64','u128','u256','u1024',
    'f8','f16','f32','f64','f128','f256','f1024'
}
COMMENT={
    '//','/*','*/'
}

TYPE={
    'int','uint','float','str','bool','null'
}
ATYPE={
    'i4','i8','i16','i32','i64','i128','i256','i1024',
    'u4','u8','u16','u32','u64','u128','u256','u1024',
    'f8','f16','f32','f64','f128','f256','f1024'
}
