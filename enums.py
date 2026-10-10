from enum import Enum

class OP(Enum):
    Add, Sub, Mul, Div, Mod, SConcat = range(6)

class PR(Enum):
    Eq, Gt, Lt, Gte, Lte = range(5)

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
}

string_to_values = dict(zip(values_to_string.values(), values_to_string.keys()))
