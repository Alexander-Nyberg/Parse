import math

def factorial(x):
    if x > 0:
        return x * factorial(x - 1)
    elif x < 0:
        raise Exception()
    else:
        return 1

# dictionary of valid constants.
constmap = {
    'true':  ('b', 1),
    'false': ('b', 0),
    'e':     ('n', math.e),
    'pi':    ('n', math.pi),
}

# dictionary of how many arguments each function expects.
fnargs = {
    'sqrt':  1,
    'cbrt':  1,
    'abs':   1,
    
    'float': 1,
    'int':   1,
    'bool':  1,
    
    'floor': 1,
    'ceil':  1,
    'trunc': 1,
    
    'pow':   2,
    
    'exp':   1,
    'exp2':  1,
    'exp10': 1,
    
    'log':   1,
    'log2':  1,
    'log10': 1,
    
    'fact':  1,
    
    'sin':   1,
    'cos':   1,
    'tan':   1,
    'asin':  1,
    'acos':  1,
    'atan':  1,
    'atan2': 2,
    
    'sinh':  1,
    'cosh':  1,
    'tanh':  1,
    'asinh': 1,
    'acosh': 1,
    'atanh': 1,
}

def expr_pow(x, y):
    if x < 0 and y != math.floor(y):
        raise Exception()
    else:
        return x ** y

# dictionary of each function that can be used in an expression.
fnmap = {
    'sqrt':  lambda x: ('n', math.sqrt(x[1])),
    'cbrt':  lambda x: ('n', math.cbrt(x[1])),
    'abs':   lambda x: ('n', x[1] if x[1] >= 0 else -x[1]),
    
    'float': lambda x: ('n', x[1]),
    'int':   lambda x: ('n', math.trunc(x[1])),
    'bool':  lambda x: ('b', 1 if x[1] else 0),
    
    'floor': lambda x: ('n', math.floor(x[1])),
    'ceil':  lambda x: ('n', math.ceil(x[1])),
    'trunc': lambda x: ('n', math.trunc(x[1])),
    
    'pow':   lambda x, y: ('n', expr_pow(x[1], y[1])),
    
    'exp':   lambda x: ('n', math.exp(x[1])),
    'exp2':  lambda x: ('n', 2.0 ** x[1]),
    'exp10': lambda x: ('n', 10.0 ** x[1]),
    
    'log':   lambda x: ('n', math.log(x[1])),
    'log2':  lambda x: ('n', math.log2(x[1])),
    'log10': lambda x: ('n', math.log10(x[1])),
    
    'fact':  lambda x: ('n', factorial(math.trunc(x[1]))),
    
    'sin':   lambda x: ('n', math.sin(x[1])),
    'cos':   lambda x: ('n', math.cos(x[1])),
    'tan':   lambda x: ('n', math.tan(x[1])),
    'asin':  lambda x: ('n', math.asin(x[1])),
    'acos':  lambda x: ('n', math.acos(x[1])),
    'atan':  lambda x: ('n', math.atan(x[1])),
    'atan2': lambda x, y: ('n', math.atan2(x[1], y[1])),
    
    'sinh':  lambda x: ('n', math.sinh(x[1])),
    'cosh':  lambda x: ('n', math.cosh(x[1])),
    'tanh':  lambda x: ('n', math.tanh(x[1])),
    'asinh': lambda x: ('n', math.asinh(x[1])),
    'acosh': lambda x: ('n', math.acosh(x[1])),
    'atanh': lambda x: ('n', math.atanh(x[1])),
}

def lex(line):
    line = line.lower()
    toks = []
    i = 0
    while True:
        if i == len(line):
            return toks
        elif line[i].isspace():
            i += 1
        elif line[i] in '0123456789':
            num = line[i]
            i += 1
            hasdot = False
            while True:
                if i == len(line):
                    break
                if line[i] == '.':
                    num += '.'
                    i += 1
                    if hasdot or i == len(line):
                        raise Exception('invalid expression!')
                    hasdot = True
                elif line[i] not in '0123456789':
                    break
                else:
                    num += line[i]
                    i += 1
            toks += [('n', float(num))]
        elif line[i] in 'abcdefghijklmnopqrstuvwxyz':
            id = line[i]
            i += 1
            while True:
                if i == len(line) or line[i] not in \
                    'abcdefghijklmnopqrstuvwxyz0123456789':
                    break
                else:
                    id += line[i]
                    i += 1
            if fnmap.get(id) is None:
                if constmap.get(id) is not None:
                    toks += [constmap[id]]
                else:
                    raise Exception(f'unknown identifier \'{id}\'!')
            else:
                toks += [('f', fnmap[id], fnargs[id])]
        elif line[i] in '+-*/%^~(),':
            toks += [(line[i], 0)]
            i += 1
        elif line[i] in '!=':
            op = line[i]
            i += 1
            if i < len(line) and line[i] == '=':
                op += '='
                i += 1
            toks += [(op, 0)]
        elif line[i] in '<>':
            op = line[i]
            i += 1
            if i < len(line) and line[i] == '=':
                op += '='
                i += 1
            elif i < len(line) and line[i] == line[i - 1]:
                op += line[i - 1]
                i += 1
            toks += [(op, 0)]
        elif line[i] in '&|':
            if i + 1 < len(line) and line[i + 1] == line[i]:
                toks += [(line[i] * 2, 0)]
                i += 2
            else:
                toks += [(line[i], 0)]
                i += 1
        else:
            raise Exception('invalid expression!')

class Parser:
    def parseor(self):
        lhs = self.parseand()
        if not len(self.toks) or self.toks[0][0] not in ['||']:
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseand()
        if op[0] in ['||']:
            self.toks = [('b', 1 if lhs[1] or rhs[1] else 0)] + self.toks
        return self.parseor()
    
    def parseand(self):
        lhs = self.parseequal()
        if not len(self.toks) or self.toks[0][0] not in ['&&']:
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseequal()
        if op[0] in ['&&']:
            self.toks = [('b', 1 if lhs[1] and rhs[1] else 0)] + self.toks
        return self.parseand()
    
    def parseequal(self):
        lhs = self.parsecmp()
        if not len(self.toks) or self.toks[0][0] not in ['=', '==', '!=']:
            return lhs
        op = self.toks.pop(0)
        rhs = self.parsecmp()
        if op[0] in ['=', '==']:
            self.toks = [('b', 1 if lhs[1] == rhs[1] else 0)] + self.toks
        elif op[0] == '!=':
            self.toks = [('b', 1 if lhs[1] != rhs[1] else 0)] + self.toks
        return self.parseequal()
    
    def parsecmp(self):
        lhs = self.parseterm()
        if not len(self.toks) or self.toks[0][0] not in ['<', '<=', '>', '>=']:
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseterm()
        if op[0] == '<':
            self.toks = [('b', 1 if lhs[1] < rhs[1] else 0)] + self.toks
        elif op[0] == '<=':
            self.toks = [('b', 1 if lhs[1] <= rhs[1] else 0)] + self.toks
        elif op[0] == '>':
            self.toks = [('b', 1 if lhs[1] > rhs[1] else 0)] + self.toks
        elif op[0] == '>=':
            self.toks = [('b', 1 if lhs[1] >= rhs[1] else 0)] + self.toks
        return self.parsecmp()
    
    def parseterm(self):
        lhs = self.parseprod()
        if not len(self.toks) or self.toks[0][0] not in '+-':
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseprod()
        if op[0] == '+':
            self.toks = [('n', lhs[1] + rhs[1])] + self.toks
        elif op[0] == '-':
            self.toks = [('n', lhs[1] - rhs[1])] + self.toks
        return self.parseterm()
    
    def parseprod(self):
        lhs = self.parsebit()
        if not len(self.toks) or self.toks[0][0] not in '*/%':
            return lhs
        op = self.toks.pop(0)
        rhs = self.parsebit()
        if op[0] == '*':
            self.toks = [('n', lhs[1] * rhs[1])] + self.toks
        elif op[0] == '/':
            self.toks = [('n', lhs[1] / rhs[1])] + self.toks
        elif op[0] == '%':
            self.toks = [('n', lhs[1] % rhs[1])] + self.toks
        return self.parseprod()
    
    def parsebit(self):
        lhs = self.parseshift()
        if not len(self.toks) or self.toks[0][0] not in '&|^':
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseshift()
        if op[0] == '&':
            self.toks = [('n', int(lhs[1]) & int(rhs[1]))] + self.toks
        elif op[0] == '|':
            self.toks = [('n', int(lhs[1]) | int(rhs[1]))] + self.toks
        elif op[0] == '^':
            self.toks = [('n', int(lhs[1]) ^ int(rhs[1]))] + self.toks
        return self.parsebit()
    
    def parseshift(self):
        lhs = self.parseunary()
        if not len(self.toks) or self.toks[0][0] not in ['<<', '>>']:
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseunary()
        if op[0] == '<<':
            self.toks = [('n', int(lhs[1]) << int(rhs[1]))] + self.toks
        elif op[0] == '>>':
            self.toks = [('n', int(lhs[1]) >> int(rhs[1]))] + self.toks
        return self.parsebit()
    
    def parseunary(self):
        if self.toks[0][0] == '+':
            self.toks.pop(0)
            return self.parseunary()
        elif self.toks[0][0] == '-':
            self.toks.pop(0)
            return ('n', -self.parseunary()[1])
        elif self.toks[0][0] == '~':
            self.toks.pop(0)
            return ('n', ~int(self.parseunary()[1]))
        elif self.toks[0][0] == '!':
            self.toks.pop(0)
            return ('b', 0 if self.parseunary()[1] else 1)
        else:
            return self.parseliteral()
    
    def parseliteral(self):
        assert self.toks[0][0] in 'fbn('
        if self.toks[0][0] == 'f':
            fn = self.toks.pop(0)
            if self.toks[0][0] == '(':
                # for functions with multiple arguments they have to be stored
                # in a list that is then used to call the function and produce
                # the expected output.
                self.toks.pop(0)
                args = [self.parseor()]
                while self.toks[0][0] == ',':
                    self.toks.pop(0)
                    args += [self.parseor()]
                assert self.toks.pop(0)[0] == ')'
                assert len(args) == fn[2]
                return fn[1](*args)
            else:
                # functions taking a single argument can be called without
                # parentheses with any expression of unary precedence or
                # higher, including other functions.
                arg = self.parseunary()
                assert fn[2] == 1
                return fn[1](arg)
        elif self.toks[0][0] in 'nb':
            return self.toks.pop(0)
        elif self.toks[0][0] == '(':
            self.toks.pop(0)
            expr = self.parseor()
            assert self.toks.pop(0)[0] == ')'
            return expr
    
    def parse(self, toks):
        try:
            self.toks = toks
            assert len(self.toks)
            result = self.parseor()
            assert not len(self.toks)
            if result[0] == 'b':
                return 'true' if result[1] else 'false'
            else:
                # make output be printed without a .0 if possible.
                rfloor = int(math.floor(result[1]))
                return str(rfloor if result[1] == rfloor else result[1])
        except:
            raise Exception('invalid expression!')

def main():
    p = Parser()
    
    while True:
        try:
            line = input('>')
            print(p.parse(lex(line)))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
