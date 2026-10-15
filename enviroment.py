from symbol import symbol_name
from settings import settings


class Env:
    def __init__(self, parent=None):
        self.values = dict()
        self.parent = parent

    def define(self, sym, value):
        if settings.immutable_mode and symbol_name(sym) in self.values:
            raise ValueError("Immutable")
        self.values[symbol_name(sym)] = value

    def get(self, sym):  # TODO сделать настройки
        cur = self
        while not (cur is None):
            if symbol_name(sym) in cur.values:
                return cur.values[symbol_name(sym)]
            cur = cur.parent
        return sym

    def set(self, sym, value):
        if settings.immutable_mode and symbol_name(sym) in self.values:
            raise ValueError("Immutable")
        cur = self
        while not (cur is None):
            if symbol_name(sym) in cur.values:
                cur.values[symbol_name(sym)] = value
                return
            cur = cur.parent
        raise NameError("Отсутствует такой симбол")
