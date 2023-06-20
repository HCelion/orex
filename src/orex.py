import re
from constants import RegexConstants, constants


class Ox(RegexConstants):
    def __init__(self, expr=None):
        super().__init__()
        if not expr:
            self.expr = r""
        else:
            self.expr = expr

    def __repr__(self):
        return f"Ox('{self.expr}')"

    def __add__(self, other):
        if isinstance(other, str):
            return Ox(expr=self.expr + other)
        return Ox(expr=self.expr + other.expr)

    def _instancer(self, pattern, starter="", ender=""):
        if isinstance(pattern, str):
            self.expr += starter + pattern + ender

        else:
            self.expr += starter + pattern.expr + ender

        return self

    def compile(
        self,
        use_ascii=False,
        dotall=False,
        ignorecase=False,
        locale=False,
        multiline=False,
    ):
        modifiers = []
        if use_ascii:
            modifiers.append(re.ASCII)
        if dotall:
            modifiers.append(re.DOTALL)
        if ignorecase:
            modifiers.append(re.IGNORECASE)
        if locale:
            modifiers.append(re.LOCALE)
        if multiline:
            modifiers.append(re.MULTILINE)
        return re.compile(self.expr, *modifiers)

    def starts_with(self, pattern):
        self._instancer(pattern, starter="^")
        return self

    def ends_with(self, pattern):
        self._instancer(pattern, ender="$")
        return self

    def is_match(self, string):
        return re.search(self.expr, string) is not None

    def findall(self, string):
        return re.findall(self.expr, string)

    def finditer(self, string):
        return re.finditer(self.expr, string)

    def get_group(self, string, name):
        match = re.search(self.expr, string)

        if match:
            return match.group(name)

        return None

    def group_dict(self, string):
        match = re.search(self.expr, string)

        if match:
            return match.groupdict()

        return None

    def sub(self, string, replacement):
        return re.sub(pattern=self.expr, repl=replacement, string=string)

    def repeat(self, pattern, n):
        ender = "){" + str(n) + "}"
        self._instancer(pattern, starter="(", ender=ender)
        return self

    @staticmethod
    def get_group_boundaries(group_identifier, lazy, capturing, name=None):

        if not capturing:
            starter = "(?:"
        else:
            if name:
                starter = f"(?P<{name}>"
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

    def one_or_more(self, pattern, lazy=False, capturing=False, name=None):

        starter, ender = self.get_group_boundaries(
            "+", lazy=lazy, capturing=capturing, name=name
        )

        self._instancer(pattern, starter=starter, ender=ender)
        return self

    def optional(self, pattern, lazy=False, capturing=False, name=None):

        starter, ender = self.get_group_boundaries(
            "?", lazy=lazy, capturing=capturing, name=name
        )
        self._instancer(pattern, starter=starter, ender=ender)
        return self

    def zero_or_one(self, pattern, lazy=False, capturing=False, name=None):
        return self.optional(pattern=pattern, lazy=lazy, capturing=capturing, name=name)

    def zero_or_more(self, pattern, lazy=False, capturing=False, name=None):
        starter, ender = self.get_group_boundaries(
            "*", lazy=lazy, capturing=capturing, name=name
        )
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

    def group(self, pattern, capturing=False, lazy=False, name=None):
        starter, ender = self.get_group_boundaries(
            "", lazy=lazy, capturing=capturing, name=name
        )
        self._instancer(pattern, starter=starter, ender=ender)
        return self

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
        self._instancer(pattern, starter="(?=.*", ender=")")
        return self

    def contains_not(self, pattern):
        self._instancer(pattern, starter="[^", ender="]")
        return self

    def reference_capturing_group(self, n=1, name=None):
        if name:
            self.expr += f"(?P={name})"
            return self
        self.expr += rf"\{n}"
        return self

    def character_class(self, pattern):
        self._instancer(pattern, starter="[", ender="]")
        return self

    def positive_lookahead_assertion(self, pattern):
        self._instancer(pattern, starter="(?=", ender=")")
        return self

    def negative_lookahead_assertion(self, pattern):
        self._instancer(pattern, starter="(?!", ender=")")
        return self


def literal(expr_str):
    return Ox(expr=expr_str)


def instancer(pattern, starter="", ender=""):
    if isinstance(pattern, str):
        expr = starter + pattern + ender
        return Ox(expr=expr)

    expr = starter + pattern.expr + ender
    return Ox(expr=expr)


def repeat(regex, n):
    ender = "){" + str(n) + "}"
    return instancer(regex, starter="(", ender=ender)


for key, value in constants.items():
    if key != "QUOTATION":
        exec(f'{key} = Ox(expr="{value}")')  # pylint: disable=(exec-used)

QUOTATION = Ox(expr='"')
