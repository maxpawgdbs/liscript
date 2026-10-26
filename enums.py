from enum import Enum


class OP(Enum):
    Add, Sub, Mul, Div, Mod, SConcat = range(6)


class PR(Enum):
    Eq, Gt, Lt, Gte, Lte = range(5)


class SF(Enum):
    (
        DEF,
        SET,
        QUOTE,
        TYPEOF,
        CONS,
        CAR,
        CDR,
        PRINT,
        READ,
        EVAL,
        COND,
        LAMBDA,
        DAMBDA,
        SYMBOL,
        DO,
        RACRO,
        DEFMACRO,
        MACROEXPAND,
        # EVALIN
    ) = range(18)


values_to_string = {
    OP.Add: "+",
    OP.Sub: "-",
    OP.Mul: "*",
    OP.Div: "/",
    OP.Mod: "%",
    OP.SConcat: "++",
    PR.Eq: "=",
    PR.Gt: ">",
    PR.Lt: "<",
    PR.Gte: ">=",
    PR.Lte: "<=",
    SF.QUOTE: "quote",
    SF.TYPEOF: "typeof",
    SF.CONS: "cons",
    SF.CAR: "car",
    SF.CDR: "cdr",
    SF.PRINT: "print",
    SF.READ: "read",
    SF.SYMBOL: "symbol",
    SF.DO: "do",
    SF.COND: "cond",
    SF.EVAL: "eval",
    SF.DEF: "def",
    SF.SET: "set!",
    SF.DAMBDA: "dambda",
    SF.LAMBDA: "lambda",
    SF.RACRO: "racro",
    SF.DEFMACRO: "defmacro",
    SF.MACROEXPAND: "macroexpand",
}

string_to_values = dict(zip(values_to_string.values(), values_to_string.keys()))
