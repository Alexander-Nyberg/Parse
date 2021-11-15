import math

constmap = {
    'e':  math.e,
    'pi': math.pi,
}

fnmap = {
    'sqrt':   lambda x: math.sqrt(x),
    'cbrt':   lambda x: math.cbrt(x),
    'abs':    lambda x: x if x >= 0 else -x,
    
    'sin':    lambda x: math.sin(x),
    'cos':    lambda x: math.cos(x),
    'tan':    lambda x: math.tan(x),
    'asin':   lambda x: math.asin(x),
    'acos':   lambda x: math.acos(x),
    'atan':   lambda x: math.atan(x),
    
    'sinh':   lambda x: math.sinh(x),
    'cosh':   lambda x: math.cosh(x),
    'tanh':   lambda x: math.tanh(x),
    'asinh':  lambda x: math.asinh(x),
    'acosh':  lambda x: math.acosh(x),
    'atanh':  lambda x: math.atanh(x),
}

def lex(line):
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
        elif line[i].lower() in 'abcdefghijklmnopqrstuvwxyz':
            id = line[i].lower()
            i += 1
            while True:
                if i == len(line) or line[i].lower() not in 'abcdefghijklmnopqrstuvwxyz':
                    break
                else:
                    id += line[i].lower()
                    i += 1
            if fnmap.get(id) is None:
                if constmap.get(id) is not None:
                    toks += [('n', constmap[id])]
                else:
                    raise Exception(f'unknown identifier \'{id}\'!')
            else:
                toks += [('f', fnmap[id])]
        elif line[i] in '+-*/%&|^~()':
            toks += [(line[i], 0)]
            i += 1
        else:
            raise Exception('invalid expression!')

class Parser:
    def parseterm(self):
        lhs = self.parseprod()
        if not len(self.toks) or self.toks[0][0] not in '+-':
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseprod()
        if op[0] == '+':
            self.toks = [('n', lhs + rhs)] + self.toks
        elif op[0] == '-':
            self.toks = [('n', lhs - rhs)] + self.toks
        return self.parseterm()
    
    def parseprod(self):
        lhs = self.parsebit()
        if not len(self.toks) or self.toks[0][0] not in '*/%':
            return lhs
        op = self.toks.pop(0)
        rhs = self.parsebit()
        if op[0] == '*':
            self.toks = [('n', lhs * rhs)] + self.toks
        elif op[0] == '/':
            self.toks = [('n', lhs / rhs)] + self.toks
        elif op[0] == '%':
            self.toks = [('n', lhs % rhs)] + self.toks
        return self.parseprod()
    
    def parsebit(self):
        lhs = self.parseunary()
        if not len(self.toks) or self.toks[0][0] not in '&|^':
            return lhs
        op = self.toks.pop(0)
        rhs = self.parseunary()
        if op[0] == '&':
            self.toks = [('n', lhs & rhs)] + self.toks
        elif op[0] == '|':
            self.toks = [('n', lhs | rhs)] + self.toks
        elif op[0] == '^':
            self.toks = [('n', lhs ^ rhs)] + self.toks
        return self.parsebit()
    
    def parseunary(self):
        if self.toks[0][0] == '+':
            self.toks.pop(0)
            return self.parseunary()
        elif self.toks[0][0] == '-':
            self.toks.pop(0)
            return -self.parseunary()
        elif self.toks[0][0] == '~':
            self.toks.pop(0)
            return ~self.parseunary()
        else:
            return self.parseliteral()
    
    def parseliteral(self):
        assert self.toks[0][0] in 'fn('
        if self.toks[0][0] == 'f':
            fn = self.toks.pop(0)[1]
            assert self.toks.pop(0)[0] == '('
            arg = self.parseterm()
            assert self.toks.pop(0)[0] == ')'
            return fn(arg)
        elif self.toks[0][0] == 'n':
            return self.toks.pop(0)[1]
        elif self.toks[0][0] == '(':
            self.toks.pop(0)
            expr = self.parseterm()
            assert self.toks.pop(0)[0] == ')'
            return expr
    
    def parse(self, toks):
        try:
            self.toks = toks
            assert len(self.toks)
            result = self.parseterm()
            assert not len(self.toks)
            return result
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
