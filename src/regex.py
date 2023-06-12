import re
from constants import RegexConstants


class Orex(RegexConstants):
    def __init__(self):
        super().__init__()
        self.expr = r""

    def compile(self):
        return self.expr

    def starts_with(self, pattern):
        if isinstance(pattern, str):
            self.expr += "^(" + pattern + ")"
        else:
            self.expr += "^(" + pattern.expr + ")"
        return self

    def ends_with(self, pattern):
        if isinstance(pattern, str):
            self.expr += "(" + pattern + ")$"
        else:
            self.expr += "(" + pattern.expr + ")$"
        return self

    def is_match(self, string):
        return re.search(self.expr, string) is not None

    def find_instances(self, string):
        return re.findall(self.expr, string)

    def repeat(self, pattern, n):
        if isinstance(pattern, str):
            self.expr += pattern * n
            return self
        # It better be an Orex pattern
        for _ in range(n):
            self.expr += pattern.expr
        return self

    def one_or_more(self, pattern):
        if isinstance(pattern, str):
            self.expr += "(" + pattern + ")+"
        else:
            self.expr += "(" + pattern.expr + ")+"
        return self

    def zero_or_more(self, pattern):
        if isinstance(pattern, str):
            self.expr += "(" + pattern + ")?"
        else:
            self.expr += "(" + pattern.expr + ")?"
        return self

    def n_or_more(self, pattern, min=None, max=None):
        # pylint: disable=(redefined-builtin)
        quantifier = r"{"

        if min:
            quantifier += str(min)

        quantifier += ","

        if max:
            quantifier += str(max)

        quantifier += "}"

        if isinstance(pattern, str):
            self.expr += "(" + pattern + ")" + quantifier

        else:
            self.expr += "(" + pattern.expr + ")" + quantifier

        return self

    def literal(self, string):
        self.expr += string

        return self

    # TODO: or and capture
