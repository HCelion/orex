import types


constants = {"WORD": r"\w", "DIGIT": "[0-9]"}


class RegexConstants:
    def __init__(self):
        self.funcs = {}
        for name, expression in constants.items():

            def new_func(self):
                self.expr += expression
                return self

            self.funcs[name] = types.MethodType(new_func, self)

    def __getattr__(self, name):
        if name in self.funcs:
            return self.funcs[name]()
        raise AttributeError(f"No such attribute: {name}")
