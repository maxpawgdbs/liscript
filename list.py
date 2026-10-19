def is_cons_list(value):
    return callable(value)


def cons(value, next):
    return lambda f: f(value, next)


fst = lambda value, next: value
snd = lambda value, next: next


# def fst(value, next):
#     return value
# def snd(value, next):
#     return next


def car(list):
    return list(fst)


def cdr(list):
    return list(snd)


nil = cons(None, None)


def is_nil(value):
    return value == nil


# fix = lambda func: lambda n: func(func, n)
# fact_core = lambda    self, n: 1 if n <= 1 else n * self(self, n - 1)
# fact = fix(fact_core)
# print(fact(7))
# print((lambda func: lambda n: func(func, n))(lambda self, n: 1 if n <= 1 else n * self(self, n - 1))(7))

# fib_core = lambda self, n: n if n <= 1 else self(self, n - 1) + self(self, n - 2)
# fib = fix(fib_core)
# print((lambda func: lambda n: func(func, n))(lambda self, n: n if n <= 1 else self(self, n - 1) + self(self, n - 2))(10))
