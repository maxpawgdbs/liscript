from list import *
from symbol import *
from enums import *

operations = {
    OP.Add: (lambda x, y: x + y),
    OP.Sub: (lambda x, y: x - y),
    OP.Mul: (lambda x, y: x * y),
    OP.Div: (lambda x, y: x / y if isinstance(x, float) or isinstance(y, float) else x // y),
    OP.Mod: (lambda x, y: x % y),
    OP.SConcat: (lambda x, y: x + y),
}


def fold_op(op, values):
    if is_nil(values):
        raise ValueError(f"Операция {values_to_string[op]} без аргументов!")
    out = eval_value(car(values))
    values = cdr(values)
    while not is_nil(values):
        elem = eval_value(car(values))
        # print(out, elem)
        out = operations[op](out, elem)
        values = cdr(values)
    return out


def eval_value(value):
    if is_cons_list(value):
        if is_nil(value):
            return value
        head = eval_value(car(value))
        if type(head) is OP:
            return fold_op(head, cdr(value))
        else:
            return value
    else:
        return value
