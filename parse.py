import re

from list import *
from symbol import *
from enums import *
import eval

def show(value):
    if type(value) is bool:
        return "true" if value else "false"
    elif value in values_to_string.keys():
        return values_to_string[value]
    elif is_symbol(value):
        return symbol_name(value)
    elif type(value) is str:
        return '"' + value + '"'
    elif is_cons_list(value):
        out = "("
        while not is_nil(value):
            out += show(car(value)) + " "
            value = cdr(value)
        if out[-1] == " ":
            out = out[:-1]
        out += ")"
        return out

    else:
        return str(value)


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
    if text in string_to_values.keys():
        return string_to_values[text]
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
    text = strip_trash_left(text)
    if text == "":
        raise ValueError("Отсутствует закрывающая скобка")
    f = text[0]
    if f == ")":
        return nil, text[1:]
    else:
        value, reminder = parser(text)
        reminder_a, reminder_b = parse_list(reminder)
        return cons(value, reminder_a), reminder_b


def parser(text):
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
    else:
        i = re.search(r"[, \n\r\t\"();]|$", text).start()
        return parse_token(text[:i]), text[i:]


def eval_text(text):
    text = strip_trash_left(text)
    while text:
        x, text = parser(text)
        x = eval.eval_value(x)
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
