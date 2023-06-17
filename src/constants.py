import types


constants = {
    "WORD_CHAR": r"\w",
    "ANY_CHAR": r".",
    "DIGIT": r"[0-9]",
    "BOUNDARY": r"\b",
    "SPACE": r"[ \t\r\n\v\f]",
    "TAB": r"\t",
    "NEWLINE": r"\n",
    "NON_WORD": r"\W",
    "RETURN": r"\r",
    "DOT": r"\.",
    "SLASH": r"\\",
    "ALPHA": r"[a-zA-Z]",
    "BLANK": r"[ \t]",
    "PUNCTUATION": r"[!\"\#$%&'()*+,\-./:;<=>?@\[\\\]^_‘{|}~]",
    "UPPER": r"[A-Z]",
    "LOWER": r"[a-z]",
    "HEXDIGIT": r"[A-Fa-f0-9]",
    "ALNUM": r"[a-zA-Z0-9]",
    "WORD": r"\b(\w+)\b",
    "QUOTAtION": '"',
}


class RegexConstants:
    def __init__(self):
        self.funcs = {}

        def make_func(expression):
            def new_func(self):
                self.expr += expression
                return self

            return new_func

        for name, expression in constants.items():
            self.funcs[name] = types.MethodType(make_func(expression), self)

    def __getattr__(self, name):
        if name in self.funcs:
            return self.funcs[name]()
        raise AttributeError(f"No such attribute: {name}")
