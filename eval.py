from list import is_nil, car, cdr, is_cons_list, cons, nil
from enums import OP, PR, SF, values_to_string
from show import repr
from symbol import is_symbol, symbol
from parser import parser
from dlambda import Lambda, Dambda
from enviroment import Env


def equal_lists(x, y):
    if not is_cons_list(x) or not is_cons_list(y):
        return False
    if is_nil(x) and is_nil(y):
        return True
    elif is_nil(x) or is_nil(y):
        return False
    head_x = car(x)
    head_y = car(y)
    while (
        (head_x == head_y and type(head_x) == type(head_y))
        if not (is_cons_list(head_x) and is_cons_list(head_y))
        else equal_lists(head_x, head_y)
    ):
        x = cdr(x)
        y = cdr(y)
        if is_nil(x) and is_nil(y):
            return True
        elif is_nil(x) or is_nil(y):
            return False
        head_x = car(x)
        head_y = car(y)
    return False


operations = {
    OP.Add: (lambda x, y: x + y),
    OP.Sub: (lambda x, y: x - y),
    OP.Mul: (lambda x, y: x * y),
    OP.Div: (
        lambda x, y: x / y if isinstance(x, float) or isinstance(y, float) else x // y
    ),
    OP.Mod: (lambda x, y: x % y),
    OP.SConcat: (lambda x, y: repr(x) + repr(y)),
}

predicate = {
    PR.Eq: (
        lambda x, y: (
            (x == y and type(x) == type(y))
            if not (is_cons_list(x) and is_cons_list(y))
            else equal_lists(x, y)
        )
    ),
    PR.Gt: (lambda x, y: x > y),
    PR.Lt: (lambda x, y: x < y),
    PR.Gte: (lambda x, y: x >= y),
    PR.Lte: (lambda x, y: x <= y),
}


def fold_op(op, values, e):
    if is_nil(values):
        raise ValueError(f"Операция {values_to_string[op]} без аргументов!")
    out = eval_value(car(values), e)
    out = repr(out) if op == OP.SConcat else out
    values = cdr(values)
    while not is_nil(values):
        elem = eval_value(car(values), e)
        # print(out, elem)
        out = operations[op](out, elem)
        values = cdr(values)
    return out


def fold_pr(pr, values, e):
    if is_nil(values):
        return True
    out = eval_value(car(values), e)
    values = cdr(values)
    while not is_nil(values):
        elem = eval_value(car(values), e)
        if not predicate[pr](out, elem):
            return False
        out = elem
        values = cdr(values)

    return True


def get_args(tail, count):
    out = []
    for _ in range(count):
        if is_nil(tail):
            raise ValueError("Недостаточно элементов в массиве")
        out.append(car(tail))
        tail = cdr(tail)

    if not is_nil(tail):
        raise ValueError("Остались лишние элементы")

    return out


DEFAULT_ARGS = symbol("rest-args")


def eval_value(value, e):
    if is_symbol(value):
        return e.get(value)
    elif is_cons_list(value):
        if is_nil(value):
            return value
        head = eval_value(car(value), e)
        if isinstance(head, OP):
            return fold_op(head, cdr(value), e)
        elif isinstance(head, PR):
            return fold_pr(head, cdr(value), e)
        elif isinstance(head, SF):
            tail = cdr(value)
            if head == SF.QUOTE:
                return get_args(tail, 1)[0]
            elif head == SF.TYPEOF:
                arg = eval_value(get_args(tail, 1)[0], e)
                if is_cons_list(arg):
                    return "list"
                elif is_symbol(arg):
                    return "symbol"
                else:
                    return type(arg).__name__
            elif head == SF.CONS:
                args = [eval_value(value, e) for value in get_args(tail, 2)]
                if not is_cons_list(args[1]):
                    raise ValueError("Хвост не список")
                return cons(args[0], args[1])
            elif head == SF.CAR:
                arg = eval_value(get_args(tail, 1)[0], e)
                if not is_cons_list(arg):
                    raise ValueError("Это не список")
                return car(arg)
            elif head == SF.CDR:
                arg = eval_value(get_args(tail, 1)[0], e)
                if not is_cons_list(arg):
                    raise ValueError("Это не список")
                return cdr(arg)
            elif head == SF.COND:
                while not is_nil(tail):
                    condition_or_value = eval_value(car(tail), e)
                    tail = cdr(tail)

                    if is_nil(tail):
                        return condition_or_value
                    if not isinstance(condition_or_value, bool):
                        raise ValueError("Ожидалось булева")

                    if condition_or_value:
                        return eval_value(car(tail), e)
                    else:
                        tail = cdr(tail)
                raise ValueError("Отсутствуют аргументы")
            elif head == SF.EVAL:
                arg = eval_value(get_args(tail, 1)[0], e)
                return eval_value(arg, e)
            elif head == SF.SYMBOL:
                arg = eval_value(get_args(tail, 1)[0], e)
                return symbol(repr(arg))
            elif head == SF.DO:
                out = nil
                while not is_nil(tail):
                    out = eval_value(car(tail), e)
                    tail = cdr(tail)
                return out
            elif head == SF.PRINT:
                out = []
                while not is_nil(tail):
                    out.append(repr(eval_value(car(tail), e)))
                    tail = cdr(tail)
                print(*out, sep=" ")
                return nil
            elif head == SF.READ:
                out = []
                while not is_nil(tail):
                    out.append(repr(eval_value(car(tail), e)))
                    tail = cdr(tail)
                user_input = input(" ".join(out))
                x, y = parser(user_input)
                return x
            elif head == SF.DEF:
                while not is_nil(tail):
                    sym = car(tail)
                    if not is_symbol(sym):
                        raise ValueError("Не симбол")

                    tail = cdr(tail)

                    if is_nil(tail):
                        raise ValueError("Отсутствует значение")

                    value = eval_value(car(tail), e)
                    e.define(sym, value)

                    tail = cdr(tail)
                return nil
            elif head == SF.SET:
                while not is_nil(tail):
                    sym = car(tail)
                    if not is_symbol(sym):
                        raise ValueError("Не симбол")

                    tail = cdr(tail)

                    if is_nil(tail):
                        raise ValueError("Отсутствует значение")

                    value = eval_value(car(tail), e)
                    e.set(sym, value)

                    tail = cdr(tail)
                return nil
            elif head == SF.LAMBDA:
                args = get_args(tail, 2)
                if not is_cons_list(args[0]):
                    raise ValueError("TODO")
                return Lambda(args[0], args[1], e)
            elif head == SF.DAMBDA:
                args = get_args(tail, 2)
                if not is_cons_list(args[0]):
                    raise ValueError("TODO")
                return Dambda(args[0], args[1])
        elif isinstance(head, Lambda):
            tail = cdr(value)
            new_e = Env(head.env)
            dambda_args = head.args
            while True:
                if is_nil(tail) and is_nil(dambda_args):
                    return eval_value(head.body, new_e)
                elif is_nil(tail):
                    return Lambda(dambda_args, head.body, new_e)
                elif is_nil(dambda_args):
                    out = []
                    while not is_nil(tail):
                        out.append(eval_value(car(tail), e))
                        tail = cdr(tail)
                    cons_out = nil
                    for el in out[::-1]:
                        cons_out = cons(el, cons_out)
                    new_e.define(DEFAULT_ARGS, cons_out)
                    return eval_value(head.body, new_e)
                arg = eval_value(car(tail), e)
                sym = car(dambda_args)

                new_e.define(sym, arg)

                tail = cdr(tail)
                dambda_args = cdr(dambda_args)
        elif isinstance(head, Dambda):
            tail = cdr(value)
            new_e = Env(e)
            dambda_args = head.args
            while True:
                if is_nil(tail) and is_nil(dambda_args):
                    return eval_value(head.body, new_e)
                elif is_nil(tail):
                    return Dambda(dambda_args, head.body)
                elif is_nil(dambda_args):
                    out = []
                    while not is_nil(tail):
                        out.append(eval_value(car(tail), e))
                        tail = cdr(tail)
                    cons_out = nil
                    for el in out[::-1]:
                        cons_out = cons(el, cons_out)
                    new_e.define(DEFAULT_ARGS, cons_out)
                    return eval_value(head.body, new_e)
                arg = eval_value(car(tail), e)
                sym = car(dambda_args)

                new_e.define(sym, arg)

                tail = cdr(tail)
                dambda_args = cdr(dambda_args)

        else:
            raise ValueError("Плохая головная форма")
    else:
        return value
