GLOBAL_ERROR_STACK = []


def raise_error_log(error):
    for el in GLOBAL_ERROR_STACK:
        print(el)
    raise ValueError(error)
