from list import is_nil, car, cdr, is_cons_list, cons, nil
from enums import OP, PR, SF, values_to_string
from show import repr
from symbol import is_symbol, symbol
from parser import parser
from enviroment import Env

env = Env()

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
    # PR.Eq: (lambda x, y: x == y and
    #                      type(x) == type(y) and
    #                      (not is_cons_list(x) or not is_cons_list(y) or equal_lists(x, y))),
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


def fold_op(op, values):
    if is_nil(values):
        raise ValueError(f"Операция {values_to_string[op]} без аргументов!")
    out = eval_value(car(values))
    out = repr(out) if op == OP.SConcat else out
    values = cdr(values)
    while not is_nil(values):
        elem = eval_value(car(values))
        # print(out, elem)
        out = operations[op](out, elem)
        values = cdr(values)
    return out


def fold_pr(pr, values):
    if is_nil(values):
        return True
    out = eval_value(car(values))
    values = cdr(values)
    while not is_nil(values):
        elem = eval_value(car(values))
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
        raise ValueError("Остались лишние элементы")  # зачем ошибка?

    return out


def eval_value(value):
    if is_symbol(value):
        return env.get(value)
    elif is_cons_list(value):
        if is_nil(value):
            return value
        head = eval_value(car(value))
        if isinstance(head, OP):
            return fold_op(head, cdr(value))
        elif isinstance(head, PR):
            return fold_pr(head, cdr(value))
        elif isinstance(head, SF):
            tail = cdr(value)
            if head == SF.QUOTE:
                return get_args(tail, 1)[0]
            elif head == SF.TYPEOF:
                arg = eval_value(get_args(tail, 1)[0])
                if is_cons_list(arg):
                    return "list"
                elif is_symbol(arg):
                    return "symbol"
                else:
                    return type(arg).__name__
            elif head == SF.CONS:
                args = list(map(eval_value, get_args(tail, 2)))
                if not is_cons_list(args[1]):
                    raise ValueError("Хвост не список")
                return cons(args[0], args[1])
            elif head == SF.CAR:
                arg = eval_value(get_args(tail, 1)[0])
                if not is_cons_list(arg):
                    raise ValueError("Это не список")
                return car(arg)
            elif head == SF.CDR:
                arg = eval_value(get_args(tail, 1)[0])
                if not is_cons_list(arg):
                    raise ValueError("Это не список")
                return cdr(arg)
            elif head == SF.COND:
                while not is_nil(tail):
                    condition_or_value = eval_value(car(tail))
                    tail = cdr(tail)

                    if is_nil(tail):
                        return condition_or_value
                    if not isinstance(condition_or_value, bool):
                        raise ValueError("Ожидалось булева")

                    if condition_or_value:
                        return eval_value(car(tail))
                    else:
                        tail = cdr(tail)
                raise ValueError("Отсутствуют аргументы")
            elif head == SF.EVAL:
                arg = eval_value(get_args(tail, 1)[0])
                return eval_value(arg)
            elif head == SF.SYMBOL:
                arg = eval_value(get_args(tail, 1)[0])
                return symbol(repr(arg))
            elif head == SF.DO:
                out = nil
                while not is_nil(tail):
                    out = eval_value(car(tail))
                    tail = cdr(tail)
                return out
            elif head == SF.PRINT:
                out = []
                while not is_nil(tail):
                    out.append(repr(eval_value(car(tail))))
                    tail = cdr(tail)
                print(*out, sep=" ")
                return nil
            elif head == SF.READ:
                out = []
                while not is_nil(tail):
                    out.append(repr(eval_value(car(tail))))
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

                    value = eval_value(car(tail))
                    env.define(sym, value)

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

                    value = eval_value(car(tail))
                    env.set(sym, value)

                    tail = cdr(tail)
                return nil
        else:
            raise ValueError("Плохая головная форма")
    else:
        return value
