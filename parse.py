from eval import eval_value
from show import show
from parser import parser, strip_trash_left


def eval_text(text, mode="text"):
    out = None
    text = strip_trash_left(text)
    while text:
        x, text = parser(text)
        x = eval_value(x)
        out = show(x)
        if mode == "text":
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
            print("Нет такого файла")
