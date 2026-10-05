def symbol(name):
    return "\0" + name


def symbol_name(sym):
    return sym[1:]


def is_symbol(value):
    return type(value) is str and value and value[0] == "\0"
