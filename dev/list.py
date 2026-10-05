# 1 реализация
class List:
    def __init__(self, value, next):
        self.value = value
        self.next = next


def is_cons_list(value):
    return type(value) is List


def cons(value, next):
    return List(value, next)


def car(list):
    return list.value


def cdr(list):
    return list.next


# 2 реализация

def is_cons_list(value):
    return type(value) is tuple


def cons(value, next):
    return (value, next)


def car(list):
    return list[0]


def cdr(list):
    return list[1]


# 3 реализация


def is_cons_list(value):
    return callable(value)


def cons(value, next):
    return lambda x: value if x == 0 else next


def car(list):
    return list(0)


def cdr(list):
    return list(1)


# 4 реализация

def is_cons_list(value):
    return callable(value)


def cons(value, next):
    return lambda f: f(value, next)


def car(list):
    return list(lambda value, next: value)


def cdr(list):
    return list(lambda value, next: next)


# общий блок
nil = cons(None, None)


def is_nil(value):
    return value == nil
