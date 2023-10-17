# constants = {
#     "WORD_CHAR": r"\w",
#     "ANY_CHAR": r".",
#     "DIGIT": r"\d",
#     "NON_DIGIT": r"\D",
#     "BOUNDARY": r"\b",
#     "SPACE": r"\s",
#     "TAB": r"\t",
#     "NEWLINE": r"\n",
#     "NON_WORD": r"\W",
#     "RETURN": r"\r",
#     "DOT": r"\.",
#     "BACKSLASH": r"\\",
#     "ALPHA": r"[a-zA-Z]",
#     "BLANK": r"[ \t]",
#     "PUNCTUATION": r"[!\"\#$%&'()*+,\-./:;<=>?@\[\\\]^_‘{|}~]",
#     "UPPER_CHAR": r"[A-Z]",
#     "LOWER_CHAR": r"[a-z]",
#     "HEXDIGIT": r"[A-Fa-f0-9]",
#     "ALNUM": r"\w",
#     "NON_ALNUM": r"\W",
#     "WORD": r"\b(\w+)\b",
#     "QUOTATION": r'"',
#     "WHITESPACE": r"\s",
#     "NON_WHITESPACE": r"\S",
#     "BAR": r"\|",
#     "START": r"^",
#     "END": r"$",
#     "DASH": r"\-",
# }

from ask_orex import Ox

WORD_CHAR = Ox("\\w")
ANY_CHAR = Ox(".")
DIGIT = Ox("\\d")
NON_DIGIT = Ox("\\D")
BOUNDARY = Ox("\\b")
SPACE = Ox("\\s")
TAB = Ox("\\t")
NEWLINE = Ox("\\n")
NON_WORD = Ox("\\W")
RETURN = Ox("\\r")
DOT = Ox("\\.")
BACKSLASH = Ox(r"\\")
ALPHA = Ox("[a-zA-Z]")
BLANK = Ox("[ \\t]")
PUNCTUATION = Ox("[!\"\\#$%&'()*+,\\-./:;<=>?@\\[\\]^_‘{|}~]")
UPPER_CHAR = Ox("[A-Z]")
LOWER_CHAR = Ox("[a-z]")
HEXDIGIT = Ox("[A-Fa-f0-9]")
ALNUM = Ox("\\w")
NON_ALNUM = Ox("\\W")
WORD = Ox("\\b(\\w+)\\b")
QUOTATION = Ox('"')
WHITESPACE = Ox("\\s")
NON_WHITESPACE = Ox("\\S")
BAR = Ox("\\|")
START = Ox("^")
END = Ox("$")
DASH = Ox("\\-")
