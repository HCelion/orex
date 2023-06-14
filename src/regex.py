import re
from constants import RegexConstants


class Orex(RegexConstants):
    def __init__(self):
        super().__init__()
        self.expr = r""

    def __repr__(self):
        return f"Orex('{self.expr}')"

    def _instancer(self, pattern, starter="", ender=""):
        if isinstance(pattern, str):
            self.expr += starter + pattern + ender

        else:
            self.expr += starter + pattern.expr + ender

        return self

    def compile(self):
        return self.expr

    def starts_with(self, pattern):
        self._instancer(pattern, starter="^")
        return self

    def ends_with(self, pattern):
        self._instancer(pattern, ender="$")
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

    def repeated(self, pattern, number):
        ender = "){" + str(number) + "}"
        self._instancer(pattern, starter="(", ender=ender)
        return self

    def one_or_more(self, pattern):
        self._instancer(pattern, starter="(", ender=")+")
        return self

    def optional(self, pattern, lazy=False):

        if lazy:
            ender = ")??"
        else:
            ender = ")?"

        self._instancer(pattern, starter="(", ender=ender)
        return self

    def zero_or_more(self, pattern):
        self._instancer(pattern, starter="(", ender=")*")
        return self

    def n_or_more(self, pattern, min=None, max=None):
        # pylint: disable=(redefined-builtin)
        quantifier = r"){"

        if min:
            quantifier += str(min)

        quantifier += ","

        if max:
            quantifier += str(max)

        quantifier += "}"

        self._instancer(pattern, starter="(", ender=quantifier)

        return self

    def literal(self, string):
        self.expr += string
        return self

    def group(self, pattern):
        self._instancer(pattern, starter="(", ender=")")
        return self

    @classmethod
    def extract_regex(cls, pattern):

        if isinstance(pattern, str):
            return pattern

        return pattern.expr

    def orex_or(self, *patterns):

        joined_patterns = "|".join([self.extract_regex(pat) for pat in patterns])

        self.expr = self.expr + "(" + joined_patterns + ")"

        return self

    def orex_and(self, pattern):

        if isinstance(pattern, str):
            self.expr = "(?=.*" + self.expr + ")(?=.*" + pattern + ")"

        else:
            self.expr = "(?=.*" + self.expr + ")(?=.*" + pattern.expr + ")"

        return self

    def orex_not(self, pattern):
        if isinstance(pattern, str):
            self.expr = "[^" + pattern + "]"

        else:
            self.expr = "[^" + pattern.expr + "]"

        return self
