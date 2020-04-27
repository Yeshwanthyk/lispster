# Types
Symbol = str
List = list
Number = (int, float)


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


program = "(begin (define r 10) (* pi (* r r)))"
ans = parse(program)
print(ans)
