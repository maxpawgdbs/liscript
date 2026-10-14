from symbol import symbol_name


class Env:
    def __init__(self):
        self.values = dict()

    def define(self, sym, value):
        # if settings.immutable_mode and symbol_name(sym) in self.values:
        #     raise ValueError("Immutable")
        self.values[symbol_name(sym)] = value

    def get(self, sym):
        return self.values.get(symbol_name(sym), sym)  # TODO сделать настройки

    def set(self, sym, value):
        # if settings.immutable_mode and symbol_name(sym) in self.values:
        #     raise ValueError("Immutable")
        self.values[symbol_name(sym)] = value
