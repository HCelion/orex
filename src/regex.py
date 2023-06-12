import re
from constants import RegexConstants


class Orex(RegexConstants):
    def __init__(self):
        super().__init__()
        self.expr = ""

    def compile(self):
        return self.expr

    def starts_with(self, inp):
        self.expr += "^" + inp
        return self

    def ends_with(self, inp):
        self.expr += inp + "$"
        return self

    def is_match(self, string):
        return re.search(self.expr, string) is not None

    def find_instances(self, string):
        return re.findall(self.expr, string)
