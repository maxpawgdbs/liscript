import re
from list import cons, nil
from enums import SF
from symbol import symbol
from enums import string_to_values


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


def parse_list(text):
    text = strip_trash_left(text)
    if text == "":
        raise ValueError("/parser.py/text/ Отсутствует закрывающая скобка")
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
            raise ValueError(
                "/parser.py/parser/ Отсутствует закрывающая кавычка в " + text[:50]
            )
        return text[: s + 1][1:-1], text[s + 1 :]
    elif f == "'":
        x, y = parser(text[1:])
        return cons(SF.QUOTE, cons(x, nil)), y
    elif f == "(":
        return parse_list(text[1:])
    elif f == ")":
        raise ValueError("/parser.py/parser/ Лишняя закрывающая скобка в " + text[:50])
    else:
        i = re.search(r"[, \n\r\t\"();]|$", text).start()
        return parse_token(text[:i]), text[i:]
