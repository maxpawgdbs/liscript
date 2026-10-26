from list import is_nil, car, cdr, is_cons_list, cons, nil
from enums import OP, PR, SF, values_to_string
from show import repr, show
from symbol import is_symbol, symbol
from parser import parser
from dlambda import Lambda, Dambda, Racro
from enviroment import Env, macro_env, env

REST_ARGS = symbol("rest-args")


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
        raise ValueError(
            f"/eval.py/fold_op/ Попытка вызвать {values_to_string[op]} без аргументов"
        )
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
            raise ValueError("/eval.py/get_args/ Недостаточно элементов в листе")
        out.append(car(tail))
        tail = cdr(tail)

    if not is_nil(tail):
        raise ValueError("/eval.py/get_args/  Остались лишние элементы в листе")

    return out


def racro_expand(value, e):
    if is_symbol(value):
        return e.get(value)
    elif is_cons_list(value):
        return (
            nil
            if is_nil(value)
            else cons(racro_expand(car(value), e), racro_expand(cdr(value), e))
        )
    else:
        return value


def macroexpand(value):
    if is_cons_list(value):
        if is_nil(value):
            return nil
        l = None
        h = car(value)
        if is_symbol(h):
            try:
                z = macro_env.get(h)
                if isinstance(z, Lambda):
                    l = z
            except Exception:
                pass
        if not (l is None):
            tail = cdr(value)
            new_env = Env(env)
            new_env.define(h, l)
            l.env.define(h, l)
            macro_args = l.args
            while True:
                if is_nil(macro_args):
                    new_env.define(REST_ARGS, tail)
                    break
                elif is_nil(tail):
                    raise ValueError(
                        f"/eval.py/macroexpand/ недостаточно аргументов для макроса"
                    )

                new_env.define(car(macro_args), car(tail))
                macro_args = cdr(macro_args)
                tail = cdr(tail)

            # print(new_env.values.keys())
            return macroexpand(eval_value(l.body, new_env))
        else:
            return cons(macroexpand(h), macroexpand(cdr(value)))
    else:
        return value


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
                    raise ValueError(
                        "/eval.py/eval_value/ cons получил вторым аргументом не лист"
                    )
                return cons(args[0], args[1])
            elif head == SF.CAR:
                arg = eval_value(get_args(tail, 1)[0], e)
                if not is_cons_list(arg):
                    raise ValueError(
                        "/eval.py/eval_value/ car получил аргументом не лист"
                    )
                return car(arg)
            elif head == SF.CDR:
                arg = eval_value(get_args(tail, 1)[0], e)
                if not is_cons_list(arg):
                    raise ValueError(
                        "/eval.py/eval_value/ cdr получил аргументом не лист"
                    )
                return cdr(arg)
            elif head == SF.COND:
                while not is_nil(tail):
                    condition_or_value = eval_value(car(tail), e)
                    tail = cdr(tail)

                    if is_nil(tail):
                        return condition_or_value
                    if not isinstance(condition_or_value, bool):
                        raise ValueError("/eval.py/eval_value/ cond получил не булеву")

                    if condition_or_value:
                        return eval_value(car(tail), e)
                    else:
                        tail = cdr(tail)
                raise ValueError(
                    "/eval.py/eval_value/ cond получил недостаточно аргументов"
                )
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
                        raise ValueError(
                            f"/eval.py/eval_value/ def получил {show(sym)} вместо симбола"
                        )

                    tail = cdr(tail)

                    if is_nil(tail):
                        raise ValueError(
                            "/eval.py/eval_value/ def получил недостаточно аргументов"
                        )

                    value = eval_value(car(tail), e)
                    e.define(sym, value)

                    tail = cdr(tail)
                return nil
            elif head == SF.SET:
                while not is_nil(tail):
                    sym = car(tail)
                    if not is_symbol(sym):
                        raise ValueError(
                            f"/eval.py/eval_value/ set! получил {show(sym)} вместо симбола"
                        )

                    tail = cdr(tail)

                    if is_nil(tail):
                        raise ValueError(
                            "/eval.py/eval_value/ set! получил недостаточно аргументов"
                        )

                    value = eval_value(car(tail), e)
                    e.set(sym, value)

                    tail = cdr(tail)
                return nil
            elif head == SF.LAMBDA:
                args = get_args(tail, 2)
                if not is_cons_list(args[0]):
                    raise ValueError(
                        "/eval.py/eval_value/ lambda получил аргументы в неверном формате"
                    )
                return Lambda(args[0], args[1], e)
            elif head == SF.DAMBDA:
                args = get_args(tail, 2)
                if not is_cons_list(args[0]):
                    raise ValueError(
                        "/eval.py/eval_value/ dambda получил аргументы в неверном формате"
                    )
                return Dambda(args[0], args[1])
            elif head == SF.RACRO:
                args = get_args(tail, 2)
                if not is_cons_list(args[0]):
                    raise ValueError(
                        "/eval.py/eval_value/ racro получил аргументы в неверном формате"
                    )
                return Racro(args[0], args[1])
            elif head == SF.DEFMACRO:
                name, args, body = get_args(tail, 3)
                macro_env.define(name, Lambda(args, body, e))
                return nil
            elif head == SF.MACROEXPAND:
                return macroexpand(tail)
        elif isinstance(head, Lambda):
            tail = cdr(value)
            new_e = Env(head.env)
            dambda_args = head.args
            while True:
                if is_nil(dambda_args):
                    out = []
                    while not is_nil(tail):
                        out.append(eval_value(car(tail), e))
                        tail = cdr(tail)
                    cons_out = nil
                    for el in out[::-1]:
                        cons_out = cons(el, cons_out)
                    new_e.define(REST_ARGS, cons_out)
                    break
                elif is_nil(tail):
                    return Lambda(dambda_args, head.body, new_e)

                arg = eval_value(car(tail), e)
                sym = car(dambda_args)

                new_e.define(sym, arg)

                tail = cdr(tail)
                dambda_args = cdr(dambda_args)

            return eval_value(head.body, new_e)

        elif isinstance(head, Dambda):
            tail = cdr(value)
            new_e = Env(e)
            dambda_args = head.args
            while True:
                if is_nil(dambda_args):
                    out = []
                    while not is_nil(tail):
                        out.append(eval_value(car(tail), e))
                        tail = cdr(tail)
                    cons_out = nil
                    for el in out[::-1]:
                        cons_out = cons(el, cons_out)
                    new_e.define(REST_ARGS, cons_out)
                    break
                elif is_nil(tail):
                    raise ValueError(
                        "/eval.py/eval_value/ dambda при вызове получил недостаточно аргументов"
                    )
                    # return Lambda(dambda_args, head.body, new_e)

                arg = eval_value(car(tail), e)
                sym = car(dambda_args)

                new_e.define(sym, arg)

                tail = cdr(tail)
                dambda_args = cdr(dambda_args)

            return eval_value(head.body, new_e)
        elif isinstance(head, Racro):
            tail = cdr(value)
            new_e = Env()
            racro_args = head.args
            while True:
                if is_nil(racro_args):
                    new_e.define(REST_ARGS, tail)
                    break
                elif is_nil(tail):
                    # raise ValueError("TODO")
                    return Racro(racro_args, racro_expand(head.body, new_e))

                new_e.define(car(racro_args), car(tail))

                tail = cdr(tail)
                racro_args = cdr(racro_args)

            return eval_value(racro_expand(head.body, new_e), e)

        else:
            raise ValueError(f"Имя не распознано как переменная или функция: {head}")
    else:
        return value
