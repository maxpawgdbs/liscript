from list import is_cons_list, is_nil, car, cdr
from symbol import symbol_name, is_symbol
from enums import values_to_string


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

    else:
        return str(value)

def repr(value):
    if type(value) is bool:
        return "true" if value else "false"
    elif value in values_to_string.keys():
        return values_to_string[value]
    elif is_symbol(value):
        return symbol_name(value)
    elif type(value) is str:
        return value
    elif is_cons_list(value):
        out = "("
        while not is_nil(value):
            out += show(car(value)) + " "
            value = cdr(value)
        if out[-1] == " ":
            out = out[:-1]
        out += ")"
        return out

    else:
        return str(value)