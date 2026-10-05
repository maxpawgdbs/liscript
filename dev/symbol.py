# 1 реализация
class Symbol:
    def __init__(self, name):
        self.name = name


def symbol(name):
    return Symbol(name)


def symbol_name(sym):
    return sym.name


def is_symbol(value):
    return type(value) is Symbol


# 2 реализация


def symbol(name):
    return "\0" + name


def symbol_name(sym):
    return sym[1:]


def is_symbol(value):
    return type(value) is str and value and value[0] == "\0"
