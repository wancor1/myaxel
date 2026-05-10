import data.data as data

def increment(ident:str) -> data.Assign:
    return data.Assign(ident,data.Expr([data.Binary(data.Variable(ident),'+',data.Literal('1'))]))

def decrement(ident:str) -> data.Assign:
    return data.Assign(ident,data.Expr([data.Binary(data.Variable(ident),'-',data.Literal('1'))]))

def let(ident:str,literal:str='0',mut:bool=False,of:str='wrap',tp:str='Null') -> data.Let:
    return data.Let(ident,data.Expr([data.Literal(literal)]),mut,of,tp)
