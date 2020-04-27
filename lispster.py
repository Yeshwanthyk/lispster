import math
import operator as op

# Types
Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict

# Parse and Tokenize


def parse(program):
    """
    Parse returns the tokens assembled into a AST

    It tokenizes the program by creating a list. This list is then fed into
    `read_from_tokens` to get the AST
    """
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):

    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')

    # Pop the first element and check if it is "(", ")" or just an atom
    token = tokens.pop(0)

    # If "(" we grab all the atoms that form the expression and put it in a
    # list.
    # We end with a list of lists of the expressions
    if token == '(':
        L = []

        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))

        tokens.pop(0)

        return L
    elif token == ")":
        raise SyntaxError("Unexpected )")
    else:
        return atom(token)


def atom(token):
    """
    We return an integer first, if that doesnt work we return it as a float.
    Otherwise it is a Symbol -> which is cast as a string
    """
    try:
        return int(token)
    except:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def tokenize(chars):
    return chars.replace("(", " ( ").replace(")", " ) ").split()

# Environment Vars


def standard_env():
    "An Environment with some Scheme procedures"

    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi ...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs':     abs,
        'append':  op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y
    })
    return env


global_env = standard_env()


# Eval

def eval(x, env=global_env):

    if isinstance(x, Symbol):
        # if its a symbol we return what it can do from the Env
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == "if":
        # We evaluate the condition, if true we pass the `conseq`
        # Otherwise we pass the `alt`
        (_, cond, cond_true, cond_false) = x
        exp = (cont_true if eval(cond, env) else cont_false)
        return eval(exp, env)
    elif x[0] == "define":
        # If something new is defined we add it to the scope by adding it
        # as a Env var
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    else:
        # Procedure call. Can be anything other than if or eval
        # We evaluate the expression and return the result
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)


program = "(begin (define r 10) (* pi (* r r)))"
ans = eval(parse(program))
print(ans)
