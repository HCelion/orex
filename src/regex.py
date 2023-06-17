import re
from constants import RegexConstants


class Ox(RegexConstants):
    def __init__(self):
        super().__init__()
        self.expr = r""

    def __repr__(self):
        return f"Ox('{self.expr}')"

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
        ender = "){" + str(n) + "}"
        self._instancer(pattern, starter="(", ender=ender)
        return self

    @staticmethod
    def get_group_boundaries(group_identifier, lazy, capturing):

        if not capturing:
            starter = "(?:"
        else:
            starter = "("

        if lazy:
            ender = f"){group_identifier}?"
        else:
            ender = f"){group_identifier}"

        return starter, ender

    def repeated(self, pattern, number):
        ender = "){" + str(number) + "}"
        self._instancer(pattern, starter="(", ender=ender)
        return self

    def one_or_more(self, pattern, lazy=False, capturing=False):

        starter, ender = self.get_group_boundaries("+", lazy=lazy, capturing=capturing)

        self._instancer(pattern, starter=starter, ender=ender)
        return self

    def optional(self, pattern, lazy=False, capturing=False):

        starter, ender = self.get_group_boundaries("?", lazy=lazy, capturing=capturing)
        self._instancer(pattern, starter=starter, ender=ender)
        return self

    def zero_or_one(self, pattern, lazy=False, capturing=False):
        return self.optional(pattern=pattern, lazy=lazy, capturing=capturing)

    def zero_or_more(self, pattern, lazy=False, capturing=False):
        starter, ender = self.get_group_boundaries("*", lazy=lazy, capturing=capturing)
        self._instancer(pattern, starter=starter, ender=ender)
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

    def group(self, pattern, capturing=False):
        if not capturing:
            starter = "(?:"
        else:
            starter = "("
        self._instancer(pattern, starter=starter, ender=")")
        return self

    @classmethod
    def extract_regex(cls, pattern):

        if isinstance(pattern, str):
            return pattern

        return pattern.expr

    def _logic_builder(self, logic, *patterns):
        pattern = [
            (pattern if isinstance(pattern, str) else pattern.expr)
            for pattern in patterns
        ]
        pattern = logic + logic.join(pattern)

        return pattern

    def orex_or(self, *patterns):
        joined_patterns = "|".join([self.extract_regex(pat) for pat in patterns])

        self.expr = self.expr + "(" + joined_patterns + ")"
        return self

    def orex_and(self, *patterns):
        pattern = self._logic_builder(")(?=.*", *patterns)
        if isinstance(pattern, str):
            self.expr = "(?=.*" + self.expr + pattern + ")"
        else:
            self.expr = (
                "(?=.*" + self.expr + pattern.expr + ")"  # pylint: disable=(no-member)
            )

        return self

    def not_literal(self, pattern):
        if isinstance(pattern, str):
            self.expr = "[^" + pattern + "]"

        else:
            self.expr = "[^" + pattern.expr + "]"

        return self
