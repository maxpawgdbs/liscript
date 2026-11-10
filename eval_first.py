from eval import eval_value, macroexpand
from show import show
from parser import parser, strip_trash_left
from enviroment import env

import errors


def eval_text(text, mode="text"):
    out = None
    text = strip_trash_left(text)
    while text:
        # errors.GLOBAL_ERROR_STACK = []
        x, text = parser(text)
        # errors.GLOBAL_ERROR_STACK.append(show(x))
        # x = macroexpand(x)
        x = eval_value(x, env)
        out = show(x)
        if mode == "text":
            # print(errors.GLOBAL_ERROR_STACK)
            print(out)
        text = strip_trash_left(text)
    if mode == "file" and not (out is None):
        print(out)


def eval_cmd(cmd):
    args = cmd.split()
    if args[0] == "l":
        try:
            with open(args[1], "r", encoding="utf8") as file:
                eval_text(file.read(), "file")
        except FileNotFoundError:
            print(f"/eval_first.py/eval_cmd/ Отсутствует файл {args[1]}")
