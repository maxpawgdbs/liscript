from list import is_nil, car, cdr, is_cons_list, cons, nil
from enums import OP, PR, SF, values_to_string
from show import repr, show
from symbol import is_symbol, symbol
from parser import parser
from dlambda import Lambda, Dambda, Racro, LazyCall
from enviroment import Env, macro_env, env
import errors

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
        errors.raise_error_log(
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
            errors.raise_error_log("/eval.py/get_args/ Недостаточно элементов в листе")
        out.append(car(tail))
        tail = cdr(tail)

    if not is_nil(tail):
        errors.raise_error_log("/eval.py/get_args/  Остались лишние элементы в листе")

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


class StackItem:
    def __init__(self, evaled, unevaled, e):
        self.evaled = evaled
        self.unevaled = unevaled
        self.e = e

    def __repr__(self):
        return "" + str(self.evaled) + " " + repr(self.unevaled)

    # def __iter__(self):
    #     yield self.evaled
    #     yield self.unevaled


def eval_iter(value, init_e, max_stack_size):
    if is_symbol(value):
        return init_e.get(value)

    if not is_cons_list(value):
        return value

    if is_nil(value):
        return value

    stack = [StackItem([], value, init_e)]
    while True:
        max_stack_size[0] = max(max_stack_size[0], len(stack))
        if not stack:
            raise ValueError("empty stack")

        # print(stack, len(stack), len(stack[-1].evaled), len(stack[-1].unevaled), end="\n\n\n\n")
        # print(stack)

        evaled = stack[-1].evaled
        unevaled = stack[-1].unevaled
        stack_e = stack[-1].e
        if is_symbol(unevaled):
            res = stack_e.get(unevaled)
            stack.pop()

            if not stack:
                return res
            else:
                stack[-1].evaled.append(res)
                continue

        elif not is_cons_list(unevaled):
            res = unevaled
            stack.pop()

            if not stack:
                return res
            else:
                stack[-1].evaled.append(res)
                continue
        elif is_nil(unevaled) and not evaled:
            stack.pop()
            if not stack:
                return nil
            stack[-1].evaled.append(nil)
            continue
        elif (
            is_nil(unevaled)
            and not isinstance(evaled[0], Lambda)
            and not isinstance(evaled[0], Racro)
            and evaled[0] != SF.EVAL
        ):
            res = apply(evaled, stack_e)
            stack.pop()

            if not stack:
                return res
            else:
                stack[-1].evaled.append(res)
                continue
        else:
            # head = car(unevaled)
            # stack[-1].unevaled = cdr(unevaled)
            # evaled_head = evaled[0] if evaled else None
            evaled_head = evaled[0] if evaled else None
            if evaled_head in (SF.EVALIN, SF.WHILE):
                res = eval_value(cons(evaled_head, unevaled), stack_e)
                stack.pop()
                if not stack:
                    return res
                stack[-1].evaled.append(res)
                continue
            if not is_nil(unevaled):
                head = car(unevaled)
                stack[-1].unevaled = cdr(unevaled)

            if evaled_head == SF.QUOTE:
                res = head
            elif (evaled_head == SF.DEF or evaled_head == SF.SET) and len(
                evaled
            ) % 2 == 1:
                res = head
            elif (
                evaled_head == SF.LAMBDA
                or evaled_head == SF.DAMBDA
                or evaled_head == SF.RACRO
            ):
                res = head
            elif evaled_head == SF.COND and (len(evaled) == 2 or is_nil(cdr(unevaled))):
                # TODO check bool
                cond_var = evaled[1] if len(evaled) >= 2 else None
                if is_nil(cdr(unevaled)) or cond_var:
                    stack.pop()
                    if is_cons_list(head):
                        stack.append(StackItem([], head, stack_e))
                        continue
                    elif is_symbol(head):
                        res = stack_e.get(head)
                    else:
                        res = head

                    if not stack:
                        return res
                else:
                    stack[-1].unevaled = cdr(unevaled)
                    stack[-1].evaled = evaled[:1]
                    continue
            elif evaled_head == SF.EVAL and is_nil(unevaled):
                # TODO check evaled[1]
                stack.pop()
                if is_cons_list(evaled[1]):
                    stack.append(StackItem([], evaled[1], stack_e))
                    continue
                elif is_symbol(evaled[1]):
                    res = stack_e.get(evaled[1])
                else:
                    res = evaled[1]

                if not stack:
                    return res
            elif isinstance(evaled_head, Lambda) and is_nil(unevaled):
                new_e = Env(evaled_head.env)
                tail_vec = evaled[1:]
                lambda_args = evaled_head.args
                big_break = False
                while True:
                    if is_nil(lambda_args):
                        rest_args = nil
                        for x in tail_vec[::-1]:
                            rest_args = cons(x, rest_args)
                        new_e.define(REST_ARGS, rest_args)
                        break
                    elif not tail_vec:
                        # TODO fix this
                        res = Lambda(lambda_args, evaled_head.body, new_e)
                        stack.pop()
                        if not stack:
                            return res
                        stack[-1].evaled.append(res)
                        big_break = True
                        break

                    new_e.define(car(lambda_args), tail_vec[0])
                    tail_vec = tail_vec[1:]
                    lambda_args = cdr(lambda_args)

                if big_break:
                    continue

                stack.pop()
                stack.append(StackItem([], evaled_head.body, new_e))
                continue

            elif isinstance(evaled_head, Racro):
                if not is_nil(unevaled):
                    res = head
                else:
                    new_e = Env(None)
                    tail_vec = evaled[1:]
                    racro_args = evaled_head.args
                    while True:
                        if is_nil(racro_args):
                            rest_args = nil
                            for x in tail_vec[::-1]:
                                rest_args = cons(x, rest_args)
                            new_e.define(REST_ARGS, rest_args)
                            break
                        elif not tail_vec:
                            # TODO fix this
                            raise ValueError("TODO")

                        new_e.define(car(racro_args), tail_vec[0])
                        tail_vec = tail_vec[1:]
                        racro_args = cdr(racro_args)

                    stack.pop()
                    stack.append(
                        StackItem([], racro_expand(evaled_head.body, new_e), stack_e)
                    )
                    continue

            elif is_cons_list(head):
                stack.append(StackItem([], head, stack_e))
                continue
            elif is_symbol(head):
                res = stack_e.get(head)
            else:
                res = head

            stack[-1].evaled.append(res)


def apply(vec, e):
    if not vec:
        raise ValueError("cant apply empty vec")

    head = vec[0]
    if isinstance(head, OP):
        # TODO empty list
        out = vec[1] if head != OP.SConcat else repr(vec[1])
        for x in vec[2:]:
            out = operations[head](out, x)
        return out
    elif isinstance(head, PR):
        if not vec:
            return True

        cur = vec[1]
        for next in vec[2:]:
            if not predicate[head](cur, next):
                return False
            cur = next
        return True

    elif isinstance(head, SF):
        tail = vec[1:]
        # TODO (def a 1 b (+ a 1))
        if head == SF.DEF:
            while tail:
                e.define(tail[0], tail[1])
                tail = tail[2:]
            return nil
        elif head == SF.SET:
            while tail:
                e.set(tail[0], tail[1])
                tail = tail[2:]
            return nil
        elif head == SF.QUOTE:
            # TODO check tail length
            return tail[0]
        elif head == SF.TYPEOF:
            if is_cons_list(tail[0]):
                return "list"
            elif is_symbol(tail[0]):
                return "symbol"
            else:
                return type(tail[0]).__name__
        elif head == SF.CONS:
            # TODO check tail length
            return cons(tail[0], tail[1])
        elif head == SF.CAR:
            # TODO check tail length
            return car(tail[0])
        elif head == SF.CDR:
            # TODO check tail length
            return cdr(tail[0])
        # elif head == enums.SF.COND:
        # elif head == enums.SF.EVAL:
        elif head == SF.PRINT:
            for x in tail:
                print(repr(x), end=" ")
            print()
        elif head == SF.READ:
            for x in tail:
                print(repr(x), end=" ")
            print()
            user_input = input()
            x, y = parser(user_input)
            return x
        elif head == SF.SYMBOL:
            return symbol(repr(tail[0]))
        elif head == SF.DO:
            return tail[-1]
        elif head == SF.LAMBDA:
            return Lambda(tail[0], tail[1], e)
        elif head == SF.DAMBDA:
            return Dambda(tail[0], tail[1])
        elif head == SF.RACRO:
            return Racro(tail[0], tail[1])
        # TODO the rest of them


def map_list(f, l):
    return nil if is_nil(l) else cons(f(car(l)), map_list(f, cdr(l)))


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
                    errors.raise_error_log(
                        f"/eval.py/macroexpand/ недостаточно аргументов для макроса"
                    )

                new_env.define(car(macro_args), car(tail))
                macro_args = cdr(macro_args)
                tail = cdr(tail)

            # print(new_env.values.keys())
            return macroexpand(eval_value(l.body, new_env))
        else:
            return map_list(macroexpand, value)
            # return cons(h, macroexpand(cdr(value)))
            # return cons(macroexpand(h), macroexpand(cdr(value)))
    else:
        return value


def eval_value(value, e, strict=True):
    if is_symbol(value):
        return e.get(value)
    with errors.error_context(value):
        if is_cons_list(value):
            if is_nil(value):
                return value
            head = eval_value(car(value), e)
            tail = cdr(value)
            if isinstance(head, OP):
                return fold_op(head, cdr(value), e)
            elif isinstance(head, PR):
                return fold_pr(head, cdr(value), e)
            elif isinstance(head, SF):

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
                        errors.raise_error_log(
                            "/eval.py/eval_value/ cons получил вторым аргументом не лист"
                        )
                    return cons(args[0], args[1])
                elif head == SF.CAR:
                    arg = eval_value(get_args(tail, 1)[0], e)
                    if not is_cons_list(arg):
                        errors.raise_error_log(
                            "/eval.py/eval_value/ car получил аргументом не лист"
                        )
                    return car(arg)
                elif head == SF.CDR:
                    arg = eval_value(get_args(tail, 1)[0], e)
                    if not is_cons_list(arg):
                        errors.raise_error_log(
                            "/eval.py/eval_value/ cdr получил аргументом не лист"
                        )
                    return cdr(arg)
                elif head == SF.COND:
                    while not is_nil(tail):
                        if is_nil(cdr(tail)):
                            return eval_value(car(tail), e, strict)

                        condition_or_value = eval_value(car(tail), e)
                        tail = cdr(tail)

                        if not isinstance(condition_or_value, bool):
                            errors.raise_error_log(
                                "/eval.py/eval_value/ cond получил не булеву"
                            )

                        if condition_or_value:
                            return eval_value(car(tail), e, strict)
                        else:
                            tail = cdr(tail)
                    errors.raise_error_log(
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
                        out = eval_value(
                            car(tail), e, strict if is_nil(cdr(tail)) else True
                        )
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
                            errors.raise_error_log(
                                f"/eval.py/eval_value/ def получил {show(sym)} вместо симбола"
                            )

                        tail = cdr(tail)

                        if is_nil(tail):
                            errors.raise_error_log(
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
                            errors.raise_error_log(
                                f"/eval.py/eval_value/ set! получил {show(sym)} вместо симбола"
                            )

                        tail = cdr(tail)

                        if is_nil(tail):
                            errors.raise_error_log(
                                "/eval.py/eval_value/ set! получил недостаточно аргументов"
                            )

                        value = eval_value(car(tail), e)
                        e.set(sym, value)

                        tail = cdr(tail)
                    return nil
                elif head == SF.LAMBDA:
                    args = get_args(tail, 2)
                    if not is_cons_list(args[0]):
                        errors.raise_error_log(
                            "/eval.py/eval_value/ lambda получил аргументы в неверном формате"
                        )
                    return Lambda(args[0], args[1], e)
                elif head == SF.DAMBDA:
                    args = get_args(tail, 2)
                    if not is_cons_list(args[0]):
                        errors.raise_error_log(
                            "/eval.py/eval_value/ dambda получил аргументы в неверном формате"
                        )
                    return Dambda(args[0], args[1])
                elif head == SF.RACRO:
                    args = get_args(tail, 2)
                    if not is_cons_list(args[0]):
                        errors.raise_error_log(
                            "/eval.py/eval_value/ racro получил аргументы в неверном формате"
                        )
                    return Racro(args[0], args[1])
                elif head == SF.DEFMACRO:
                    name, args, body = get_args(tail, 3)
                    macro_env.define(name, Lambda(args, body, e))
                    return nil
                elif head == SF.MACROEXPAND:
                    return macroexpand(tail)
                elif head == SF.WHILE:
                    condition = car(tail)
                    body = cdr(tail)
                    while eval_value(condition, e):
                        t = body
                        while not is_nil(t):
                            eval_value(car(t), e)
                            t = cdr(t)
                    return nil
                elif head == SF.ERROR:
                    out = []
                    while not is_nil(tail):
                        out.append(repr(eval_value(car(tail), e)))
                        tail = cdr(tail)
                    errors.raise_error_log(" ".join(str(x) for x in out))
                elif head == SF.EVALIN:
                    env_lambda = eval_value(car(tail), e)
                    if not isinstance(env_lambda, Lambda):
                        errors.raise_error_log("Ожидалась лямбда")
                    tail = cdr(tail)
                    out = nil
                    while not is_nil(tail):
                        out = eval_value(
                            car(tail),
                            env_lambda.env,
                            strict if is_nil(cdr(tail)) else True,
                        )
                        tail = cdr(tail)
                    return out
                elif head == SF.PYTHON:
                    out = nil
                    while not is_nil(tail):
                        k = eval_value(car(tail), e)
                        if not isinstance(k, str):
                            errors.raise_error_log("Ожидалась строка")
                        out = eval(k)
                        tail = cdr(tail)
                    return out
            elif isinstance(head, Lambda):
                # tail = cdr(value)
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

                # return eval_value(head.body, new_e)
                out = LazyCall(head.body, new_e)
                if strict:
                    while isinstance(out, LazyCall):
                        out = eval_value(out.expr, out.env, False)
                return out

            elif isinstance(head, Dambda):
                # tail = cdr(value)
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
                        errors.raise_error_log(
                            "/eval.py/eval_value/ dambda при вызове получил недостаточно аргументов"
                        )
                        # return Lambda(dambda_args, head.body, new_e)

                    arg = eval_value(car(tail), e)
                    sym = car(dambda_args)

                    new_e.define(sym, arg)

                    tail = cdr(tail)
                    dambda_args = cdr(dambda_args)

                out = LazyCall(head.body, new_e)
                if strict:
                    while isinstance(out, LazyCall):
                        out = eval_value(out.expr, out.env, False)
                return out
            elif isinstance(head, Racro):
                # tail = cdr(value)
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
            elif callable(head):
                args = []
                while not is_nil(tail):
                    args.append(eval_value(car(tail), e))
                    tail = cdr(tail)
                return head(*args)
            else:
                try:
                    arg = eval_value(get_args(tail, 1)[0], e)
                    return getattr(head, arg)
                except Exception:
                    errors.raise_error_log(
                        f"Имя не распознано как переменная или функция: {head}"
                    )
        else:
            return value
