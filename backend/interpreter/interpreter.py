import backend.interpreter.environment as environment
import data.data as data

class Interpreter:
    def __init__(self):
        self.env=environment.Environment()

    def eval(self,node):
        if isinstance(node,data.Literal):
            return 
        elif isinstance(node,data.Variable):
            pass
        elif isinstance(node,data.Expr):
            pass
