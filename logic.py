
def symbol(sym):
    def symbol_wrapper(func):
        func.symbol = sym 
        print(func.symbol)
        return func
    return symbol_wrapper

class Operation:
    @staticmethod
    @symbol('')
    def NOOP(x, y):
        assert y is None
        return x

    @staticmethod
    @symbol(' | ')
    def OR(x, y):
        assert None not in (x, y)
        return bool(x or y)

    @staticmethod
    @symbol(' & ')
    def AND(x, y):
        assert None not in (x, y)
        return bool(x and y)

    @staticmethod
    @symbol('~')
    def NOT(x, y):
        assert y is None 
        return not x

    @staticmethod
    @symbol(' ^ ')
    def XOR(x, y):
        assert None not in (x, y)
        return x ^ y

class Expr:
    def __init__(self, left, op=Operation.NOOP, right=None):
        self.left = left 
        self.op = op 
        self.right = right

    @staticmethod 
    def sub(variables, expr):
        if isinstance(expr, Expr):
            return expr.eval(variables)
        elif expr is None:
            return expr
        else:
            return variables[expr]

    def eval(self, variables):
        left = self.sub(variables, self.left)
        right = self.sub(variables, self.right)

        return self.op(left, right)

    def __add__(self, other):
        if not isinstance(other, Expr):
            return NotImplemented
        return Expr(self, Operation.OR, other)

    def __mul__(self, other):
        if not isinstance(other, Expr):
            return NotImplemented
        return Expr(self, Operation.AND, other)

    def __invert__(self):
        return Expr(self, Operation.NOT)

    def __xor__(self, other):
        if not isinstance(other, Expr):
            return NotImplemented
        return Expr(self, Operation.XOR, other)

    def __bool__(self):
        raise TypeError()

    def __str__(self):
        r = str(self.right) if self.right is not None else ''
        s = self.op.symbol
        l = str(self.left)
        if r:
            return '(' + l + s + r + ')'
        return s + l

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.left)}, {self.op.__name__}, {repr(self.right)})'
        

def variables(names):
    names = names.split(' ')
    return [Expr(n.strip(', ')) for n in names]

def print_truth_table(expr, variables):
    s = lambda binary: str(binary).replace('0', '-').replace('1', '#')

    for v in variables:
        print(s(v), end=' ')
    print('   ', end='')
    print(expr)
    for permutation in range(2**len(variables)):
        these_vars = {v: permutation >> i & 1 for i, v in enumerate(reversed(variables)) }
        for v in variables:
            print(s(these_vars[v]), end=' ')
        print('   ', end='')
        print(s(expr.eval(these_vars) & 1))
        

if __name__ == "__main__":
    a, b, c, d = (variables('A B C D'))
    expr = ~a*b*(~d+~c*d) + b*(a+~a*c*d)
    print_truth_table(expr, 'ABCD')
    print_truth_table(a ^ b, 'AB')
    print(repr(expr))