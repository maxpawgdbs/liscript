# error_stack.py
from contextlib import contextmanager

GLOBAL_ERROR_STACK = []


@contextmanager
def error_context(expression):
    GLOBAL_ERROR_STACK.append(expression)
    try:
        yield
    except Exception as error:
        if not hasattr(error, "liscript_stack"):
            error.liscript_stack = GLOBAL_ERROR_STACK.copy()
        raise
    finally:
        GLOBAL_ERROR_STACK.pop()


def raise_error_log(error):
    raise ValueError(error)


def print_error_log(error):
    from show import show

    for expression in getattr(error, "liscript_stack", ()):
        print(f"\033[31m{show(expression)}\033[0m")
    print(f"\033[31m{error}\033[0m")
