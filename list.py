# def is_cons_list(value):
#     return callable(value)
#
#
# def cons(value, next):
#     return lambda f: f(value, next)
#
#
# fst = lambda value, next: value
# snd = lambda value, next: next
#
#
# def car(list):
#     if is_nil(list):
#         raise ValueError("car от пустого списка")
#     return list(fst)
#
#
# def cdr(list):
#     if is_nil(list):
#         raise ValueError("cdr от пустого списка")
#     return list(snd)
#
#
# nil = cons(None, None)
#
#
# def is_nil(value):
#     return value == nil
#

def is_cons_list(value):
    return type(value) is tuple


def cons(value, next):
    return (value, next)


def car(list):
    if is_nil(list):
        raise ValueError("car от пустого списка")
    return list[0]


def cdr(list):
    if is_nil(list):
        raise ValueError("cdr от пустого списка")
    return list[1]


nil = cons(None, None)


def is_nil(value):
    return value == nil
