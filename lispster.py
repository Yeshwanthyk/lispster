def tokenize(chars):
    return chars.replace("(", " ( ").replace(")", " ) ").split()
