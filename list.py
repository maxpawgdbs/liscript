def is_cons_list(value):
    return callable(value)


def cons(value, next):
    return lambda f: f(value, next)


def car(list):
    return list(lambda value, next: value)


def cdr(list):
    return list(lambda value, next: next)


nil = cons(None, None)


def is_nil(value):
    return value == nil
