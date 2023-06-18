import types


constants = {
    "WORD_CHAR": r"\w",
    "ANY_CHAR": r".",
    "DIGIT": r"\d",
    "NON_DIGIT": r"\D",
    "BOUNDARY": r"\b",
    "SPACE": r"[ \t\r\n\v\f]",
    "TAB": r"\t",
    "NEWLINE": "\n",
    "NON_WORD": r"\W",
    "RETURN": r"\r",
    "DOT": r"\.",
    "BACKSLASH": r"\\",
    "ALPHA": r"[a-zA-Z]",
    "BLANK": r"[ \t]",
    "PUNCTUATION": r"[!\"\#$%&'()*+,\-./:;<=>?@\[\\\]^_‘{|}~]",
    "UPPER_CHAR": r"[A-Z]",
    "LOWER_CHAR": r"[a-z]",
    "HEXDIGIT": r"[A-Fa-f0-9]",
    "ALNUM": r"\w",
    "NON_ALNUM": r"\W",
    "WORD": r"\b(\w+)\b",
    "QUOTAtION": '"',
    "WHITESPACE": r"\s",
    "NON_WHITESPACE": r"\S",
    "BAR": r"\|",
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
