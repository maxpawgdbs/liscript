from list import is_cons_list, is_nil, car, cdr
from symbol import symbol_name, is_symbol
from enums import values_to_string, SF
from lambdadambda import Lambda, Dambda


def show(value):
    if type(value) is bool:
        return "true" if value else "false"
    elif value in values_to_string.keys():
        return values_to_string[value]
    elif is_symbol(value):
        return symbol_name(value)
    elif type(value) is str:
        return '"' + value + '"'
    elif is_cons_list(value):
        out = "("
        while not is_nil(value):
            out += show(car(value)) + " "
            value = cdr(value)
        if out[-1] == " ":
            out = out[:-1]
        out += ")"
        return out
    elif type(value) is Lambda:
        return f"({values_to_string[SF.LAMBDA]} {show(value.args)} {show(value.body)})"
    elif type(value) is Dambda:
        return f"({values_to_string[SF.DAMBDA]} {show(value.args)} {show(value.body)})"
    else:
        return str(value)


def repr(value):
    return value if isinstance(value, str) else show(value)
