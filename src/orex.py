import re
from constants import constants


class Ox:
    def __init__(self, expr=None):
        super().__init__()
        if not expr:
            self.expr = r""
        else:
            self.expr = expr

    def __repr__(self):
        return f"Ox('{self.expr}')"

    def __add__(self, other):
        other = extract_regex(other)
        return Ox(expr=self.expr + other)

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
        if isinstance(replacement, str):
            return re.sub(pattern=self.expr, repl=replacement, string=string)
        # Regexes are a fair replacement as well
        return re.sub(pattern=self.expr, repl=replacement.expr, string=string)

    def split(self, s, max_split=None):
        if max_split:
            return re.compile(self.expr).split(s, max_split)
        return re.compile(self.expr).split(s)


def literal(expr_str):
    return Ox(expr=expr_str)


def instancer(pattern, starter="", ender=""):
    if isinstance(pattern, str):
        expr = starter + pattern + ender
        return Ox(expr=expr)

    expr = starter + pattern.expr + ender
    return Ox(expr=expr)


def extract_regex(pattern):

    if isinstance(pattern, str):
        return pattern

    return pattern.expr


def logic_builder(logic, *patterns):
    pattern = [
        (pattern if isinstance(pattern, str) else pattern.expr) for pattern in patterns
    ]
    pattern = logic + logic.join(pattern)

    return pattern


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


def repeat(regex, n):
    ender = "){" + str(n) + "," + str(n) + "}"
    return instancer(regex, starter="(?:", ender=ender)


def one_or_more(pattern, lazy=False, capturing=False, name=None):

    starter, ender = get_group_boundaries(
        "+", lazy=lazy, capturing=capturing, name=name
    )

    return instancer(pattern, starter=starter, ender=ender)


def group(pattern, capturing=False, lazy=False, name=None):
    starter, ender = get_group_boundaries("", lazy=lazy, capturing=capturing, name=name)
    return instancer(pattern, starter=starter, ender=ender)


def orex_or(*patterns):
    joined_patterns = "|".join([extract_regex(pat) for pat in patterns])
    return Ox("(" + joined_patterns + ")")


def n_or_more(pattern, min=None, max=None):
    # pylint: disable=(redefined-builtin)
    quantifier = r"){"

    if min:
        quantifier += str(min)

    quantifier += ","

    if max:
        quantifier += str(max)

    quantifier += "}"

    return instancer(pattern, starter="(?:", ender=quantifier)


def optional(pattern, lazy=False, capturing=False, name=None):

    starter, ender = get_group_boundaries(
        "?", lazy=lazy, capturing=capturing, name=name
    )
    return instancer(pattern, starter=starter, ender=ender)


def zero_or_more(pattern, lazy=False, capturing=False, name=None):
    starter, ender = get_group_boundaries(
        "*", lazy=lazy, capturing=capturing, name=name
    )
    return instancer(pattern, starter=starter, ender=ender)


def capture(pattern, name=None, lazy=False):
    starter, ender = get_group_boundaries("", lazy=lazy, capturing=True, name=name)
    return instancer(pattern, starter=starter, ender=ender)


def NOT(pattern):
    return instancer(pattern, starter="[^", ender="]")


def orex_and(*patterns):
    pattern = logic_builder(")(?=.*", *patterns)
    return instancer(pattern, starter="(?=.*", ender=")")


def reference_capturing_group(n=1, name=None):
    if name:
        return Ox(f"(?P={name})")
    return Ox(rf"\{n}")


def character_class(pattern):
    return instancer(pattern, starter="[", ender="]")


def positive_lookahead_assertion(pattern):
    return instancer(pattern, starter="(?=", ender=")")


def negative_lookahead_assertion(pattern):
    return instancer(pattern, starter="(?!", ender=")")


for key, value in constants.items():
    if key != "QUOTATION":
        exec(f'{key} = Ox(expr="{value}")')  # pylint: disable=(exec-used)
        # exec(f'Ox.{key} = Ox(expr="{value}")')  # pylint: disable=(exec-used)


QUOTATION = Ox(expr='"')
# Needed to be coded by hand, as otherwise it gets problematic
BOUNDARY = Ox(expr=r"\b")
WORD = Ox(expr=r"\b(\w+)\b")
BACKSLASH = Ox(r"\\")
END = Ox(r"$")
