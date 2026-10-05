import re

from print_funcs import *


# print(show(1), show(1.11), show("agds"), show(True), show(False))
#
# l = cons(1, nil)
# l = cons(symbol("1gg3"), l)
# l = cons(symbol("af1_a"), l)
# l = cons("413ff _//", l)
# for i in range(2, 11):
#     l = cons(i, l)
# l = cons(l, l)
# print(show(l))

def strip_trash_left(text):
    while len(text) > 0:
        if text[0] in ", \n\r\t":
            text = text[1:]
        elif text[0] == ";":
            s = text.find("\n")
            if s == -1:
                return ""
            text = text[s:]
        else:
            return text
    return text


def parse_token(text):
    if text == "true":
        return True
    elif text == "false":
        return False
    try:
        return int(text)
    except Exception:
        try:
            return float(text)
        except Exception:
            return symbol(text)


def parse_list(text):
    # print("parse_list:", text)
    text = strip_trash_left(text)
    if text == "":
        raise ValueError("Отсутствует закрывающая скобка")
    f = text[0]
    if f == ")":
        return nil, text[1:]
    # elif f.isspace() or f == ",":
    #     return parse_list(text[1:])
    # elif f == ";":
    #     s = text.find("\n")
    #     # print(s)
    #     if s == -1:
    #         return None, ""
    #     return parse_list(text[s:])
    else:
        value, reminder = parser(text)
        reminder_a, reminder_b = parse_list(reminder)
        return cons(value, reminder_a), reminder_b


def parser(text):
    # print("parser:", text)
    text = strip_trash_left(text)
    if text == "":
        return None, ""
    f = text[0]
    if f == '"':
        s = text[1:].find('"') + 1
        if s == 0:
            raise ValueError("Отсуствует закрывающая кавычка в " + text[:50])
        return text[:s + 1][1:-1], text[s + 1:]
    elif f == "(":
        return parse_list(text[1:])
    elif f == ")":
        raise ValueError("Лишняя закрывающая скобка в " + text[:50])
    # elif f.isspace() or f == ",":
    #     return parser(text[1:])
    # elif f == ";":
    #     s = text.find("\n")
    #     # print(s)
    #     if s == -1:
    #         return None, ""
    #     return parser(text[s:])
    else:
        i = re.search(r"[, \n\r\t\"();]|$", text).start()
        # print(i)
        return parse_token(text[:i]), text[i:]


# text = """ ,,,,,; comment
# (; comment
# 44,   , \"41343.1\" , , , (,, , , 22\n
# \n\n,,, ( , ,, 33 fggg; comment
# ) , , , ,( weew , 1e7 inf, , .0, ,); comment
# (;\n\n ; comment
# \n\n) , ,()) , ,5 5.0) ,,
# ,,,,,; comment"""
# # text = "123;comment"
# # text = "(123 123)"
# x, y = parser(text)
# print(show(x))
# print(y)
# print(show(parser(text)))
# print(parser(text))
# ; comment
# x, y = parser("1 2 3")
# print(show(x))
# print(y)
# print(parser("1 2 3"))

def eval_text(text):
    # print(text)
    text = strip_trash_left(text)
    while text:
        # print(text)
        x, text = parser(text)
        print(show(x))
        text = strip_trash_left(text)

def eval_cmd(cmd):
    args = cmd.split()
    if args[0] == "l":
        try:
            with open(args[1], "r", encoding="utf8") as file:
                eval_text(file.read())
        except FileNotFoundError:
            print("Нет такого файла")

def RPL():
    while True:
        cmd = input(">> ")
        # print([cmd])
        try:
            if cmd and cmd[0] == ":":
                eval_cmd(cmd[1:])
            else:
                eval_text(cmd)
        except Exception as e:
            print(e)

