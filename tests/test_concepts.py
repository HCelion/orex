# pylint: skip-file
# flake8: noqa

import re
import pytest
import orex as ox
from orex import Ox


def test_constants_can_be_found():

    s = "foo123bar"

    pattern = ox.DIGIT + ox.DIGIT + ox.DIGIT

    result = re.search(pattern.compile(), s)
    assert result is not None

    results = re.findall(pattern.compile(), s)
    assert len(results) == 1
    assert results[0] == "123"


def test_starts_with():

    s = "foo123bar"

    pattern = ox.START + "f"
    assert pattern.is_match(s)

    pattern2 = ox.START + "b"
    assert not pattern2.is_match(s)


def test_ends_with():

    s = "foo123bar"

    pattern = ox.literal("r") + ox.END
    assert pattern.is_match(s)

    pattern = ox.literal("2") + ox.END
    assert not pattern.is_match(s)


def test_findall():
    s = "foo123bar345"
    pattern = ox.DIGIT + ox.DIGIT + ox.DIGIT
    results = pattern.findall(s)

    assert len(results) == 2
    assert results[0] == "123"
    assert results[1] == "345"


def test_repeat_on_string():
    s = "foo111bar"
    assert ox.repeat("1", 3).is_match(s)
    s = "foo123bar"
    assert not ox.repeat("1", 3).is_match(s)


def test_repeat_on_pattern():
    s = "foo123bar"
    assert ox.repeat(ox.DIGIT, 3).is_match(s)

    s = "foo12bar"
    assert not ox.repeat(ox.DIGIT, 3).is_match(s)


def test_one_or_more_str():
    s = "foo123bar"
    pattern = ox.one_or_more(ox.repeat(ox.DIGIT, 3))

    assert pattern.is_match(s)

    s = "foo123456bar"
    assert pattern.is_match(s)

    s = "foo12bar"
    assert not pattern.is_match(s)


def test_one_or_more_pattern():
    s = "foo123bar"
    assert ox.one_or_more(ox.DIGIT + ox.DIGIT + ox.DIGIT).is_match(s)

    s = "foo12bar"
    assert not ox.one_or_more(ox.DIGIT + ox.DIGIT + ox.DIGIT).is_match(s)


def test_one_or_more_laziness():
    s = "<EM>first</EM>"

    pattern = ox.literal("<") + ox.one_or_more(ox.ANY_CHAR) + ">"
    results = pattern.findall(s)
    assert results[0] == "<EM>first</EM>"

    pattern = ox.literal("<") + ox.one_or_more(ox.ANY_CHAR, lazy=True) + ">"
    results = pattern.findall(s)
    assert len(results) == 2
    assert results[0] == "<EM>"
    assert results[1] == "</EM>"


def test_blank():
    s = "foo123bar"
    assert not ox.BLANK.is_match(s)

    s = "foo 123bar"
    assert ox.BLANK.is_match(s)

    s = "foo    123bar"
    assert ox.BLANK.is_match(s)


def test_n_or_more_string():
    s = "foo123bar"
    assert ox.n_or_more("o", min=2).is_match(s)

    s = "foo123bar"
    assert not ox.n_or_more("o", min=3).is_match(s)

    s = "foooo123bar"
    assert ox.n_or_more("o", min=1, max=4).is_match(s)

    s = "foooo0123bar"
    assert not ox.n_or_more("o", min=6, max=7).is_match(s)


def test_n_or_more_digit():
    s = "foo123bar"
    assert ox.n_or_more(ox.DIGIT, min=2).is_match(s)

    s = "foo123bar"
    assert not ox.n_or_more(ox.DIGIT, min=4).is_match(s)

    s = "foooo123bar"
    assert ox.n_or_more(ox.DIGIT, min=1, max=4).is_match(s)

    s = "foooo0123bar"
    assert not ox.n_or_more(ox.DIGIT, min=6, max=7).is_match(s)


def test_word():
    s = " word "
    assert ox.WORD.is_match(s)

    pattern_alt = ox.BOUNDARY + ox.one_or_more(ox.WORD_CHAR) + ox.BOUNDARY
    assert pattern_alt.is_match(s)

    results = ox.WORD.findall(s)
    assert len(results) == 1
    assert results[0] == "word"

    results = pattern_alt.findall(s)
    assert len(results) == 1
    assert results[0] == "word"

    s = " word test"
    results = ox.WORD.findall(s)
    assert len(results) == 2
    assert results[0] == "word"
    assert results[1] == "test"

    results = pattern_alt.findall(s)
    assert len(results) == 2
    assert results[0] == "word"
    assert results[1] == "test"


def test_literal():
    s = "about cats and dogs"
    assert ox.literal("cat").is_match(s)

    assert not ox.literal("rat").is_match(s)


def test_literal_takes_regex():
    s = "This is 1999"
    pattern = ox.literal("[1-9]") + ox.repeat(ox.literal("[0-9]"), 3)
    assert pattern.is_match(s)

    pattern = ox.literal("[1-9]") + ox.repeat("[0-9]", 3)
    assert pattern.is_match(s)


def test_or():
    s = "the cat in in the house"

    assert ox.orex_or("cat", "dog").is_match(s)
    assert ox.orex_or(ox.literal("cat"), ox.literal("dog")).is_match(s)

    s = "the dog in in the house"
    assert ox.orex_or("cat", "dog").is_match(s)

    s = "the rat in in the house"
    assert not ox.orex_or("cat", "dog").is_match(s)


def test_optional():

    s = "We meet in February!"

    pattern = ox.literal("Feb") + ox.optional("ruary")
    assert pattern.is_match(s)

    s = "We meet on Feb 19th!"
    assert pattern.is_match(s)

    s = "We dont meet in March!"
    assert not pattern.is_match(s)

    s = "We dont meet in a B ruary!"
    assert not pattern.is_match(s)


def test_optional_laziness():
    s = "We meet in February!"

    pattern = ox.group(
        ox.literal("Feb") + ox.optional("ruary", capturing=True), capturing=True
    )

    results = pattern.findall(s)
    assert len(results) == 1
    assert ("February", "ruary") in results

    pattern = ox.group(
        ox.literal("Feb") + ox.optional("ruary", lazy=True, capturing=True),
        capturing=True,
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert ("Feb", "") in results


def test_not_pattern():
    s = '"string one" and "string two"'
    pattern = (
        ox.literal('"')
        + ox.zero_or_more(
            ox.NOT(ox.RETURN + ox.QUOTATION + ox.NEWLINE), capturing=False
        )
        + ox.literal('"')
    )
    results = pattern.findall(s)
    assert len(results) == 2
    assert results[0] == '"string one"'
    assert results[1] == '"string two"'


def test_capturing_in_optional():
    s = "SetValue"

    results = (ox.literal("Set") + ox.optional("Value")).findall(s)
    assert results[0] == "SetValue"

    results = (ox.literal("Set") + ox.optional("Value", capturing=False)).findall(s)
    assert results[0] == "SetValue"

    results = (ox.literal("Set") + ox.optional("Value", capturing=True)).findall(s)
    assert results[0] == "Value"


def test_orex_and():
    s = "foo123bar"
    assert ox.orex_and("foo", "bar").is_match(s)
    assert ox.orex_and("foo", ox.literal("bar"))
    assert ox.orex_and("foo", "bar", "123").is_match(s)
    assert ox.orex_and("123", "bar", "foo").is_match(s)
    assert not ox.orex_and("foo", "baz").is_match(s)
    assert not ox.orex_and("qux", "bar", "foo").is_match(s)


def test_orex_or():
    s = "foo123bar"
    assert ox.orex_or("foo", ox.literal("baz")).is_match(s)
    assert ox.orex_or("foo", ox.orex_or("baz")).is_match(s)
    assert ox.orex_or("foo", "baz").is_match(s)
    assert ox.orex_or("baz", "foo").is_match(s)
    assert ox.orex_or("baz", "qux", "123").is_match(s)
    assert ox.orex_or("123", "qux", "baz").is_match(s)


def test_back_reference():
    s = "<EM>first</EM>"

    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True)
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True)
        + ox.literal("</")
        + ox.reference_capturing_group()
        + ox.literal(">")
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")

    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True)
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True)
        + ox.literal("</")
        + ox.reference_capturing_group(1)  # Here we explicitly reference 1st group
        + ox.literal(">")
    )

    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")

    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True)
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True)
        + ox.literal("</")
        + ox.reference_capturing_group(2)  # Here we explicitly reference 1st group
        + ox.literal(">")
    )
    assert not pattern.is_match(s)

    s = "<EM>first</first>"
    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True)
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True)
        + ox.literal("</")
        + ox.reference_capturing_group(2)  # Here we explicitly reference 2nd  group
        + ox.literal(">")
    )
    assert pattern.is_match(s)


def test_named_back_reference():
    s = "<EM>first</EM>"

    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True, name="tag")
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True)
        + ox.literal("</")
        + ox.reference_capturing_group(
            name="tag"
        )  # Here we explicitly reference 2nd  group
        + ox.literal(">")
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")


def test_optional_special_case():
    s = "b"
    # (q?)b\1 does typically not match as the empty group does not back reference
    pattern = (
        ox.optional("q", capturing=True)
        + ox.literal("b")
        + ox.reference_capturing_group()
    )
    assert not pattern.is_match(s)
    # (q)?b\1 does typically match
    pattern = (
        ox.group(ox.literal("q?"), capturing=True)
        + ox.literal("b")
        + ox.reference_capturing_group()
    )
    assert pattern.is_match(s)
    pattern = (
        ox.group(ox.optional("q", capturing=False), capturing=True)
        + ox.literal("b")
        + ox.reference_capturing_group()
    )
    assert pattern.is_match(s)


def test_forward_referencing_does_not_work_in_python():
    s = "oneonetwo"
    pattern = ox.one_or_more(
        ox.orex_or(
            ox.reference_capturing_group(2) + ox.literal("two"),
            ox.group(ox.literal("one"), capturing=True),
        ),
        capturing=True,
    )

    try:
        pattern.is_match(s)
    except:
        assert True


def test_character_class():

    s = "This costs 12$"

    pattern = ox.repeat(ox.DIGIT, 2) + ox.literal("$")
    # the $ is interpreted as meaning end of string
    assert not pattern.is_match(s)

    pattern = ox.repeat(ox.DIGIT, 2) + ox.character_class("$")
    assert pattern.is_match(s)


def test_backslash():
    s = r"this is a \string in latex"
    pattern = ox.BACKSLASH + ox.literal("string")
    assert pattern.is_match(s)


def test_match_new_line():
    s = """This has a
    new line"""
    assert ox.NEWLINE.is_match(s)


def test_find_iter():
    s = "12 drummers drumming, 11 pipers piping, 10 lords a-leaping"
    iterator = (ox.DIGIT + ox.DIGIT).finditer(s)

    counter = 0
    for match in iterator:
        assert int(match.group()) > 9
        counter += 1
    assert counter == 3


def test_replacement():
    s = "12 drummers drumming, 11 pipers piping, 10 lords a-leaping"
    pattern = ox.DIGIT + ox.DIGIT

    result = pattern.sub(s, "aa")
    assert result == "aa drummers drumming, aa pipers piping, aa lords a-leaping"
    # The original string is not altered
    assert s == "12 drummers drumming, 11 pipers piping, 10 lords a-leaping"


def test_advanced_subbing():
    s = "section{First} section{second}"
    pattern = ox.literal("section{") + ox.capture(ox.zero_or_more(ox.NOT("}"))) + "}"
    replacement = ox.literal("subsection{") + ox.reference_capturing_group() + "}"
    substitution = pattern.sub(s, replacement=replacement)
    assert substitution == "subsection{First} subsection{second}"


def test_compilation():
    import re

    s = " test "
    s_alt = " TEST "
    pattern = ox.literal("test").compile()
    assert re.search(pattern, s)
    assert not re.search(pattern, s_alt)

    pattern = ox.literal("test").compile(ignorecase=True)
    assert re.search(pattern, s)
    assert re.search(pattern, s_alt)


def test_named_groups():
    s = "<EM>first</EM>"

    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True, name="tag")
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True)
        + ox.literal("</")
        + ox.reference_capturing_group(
            name="tag"
        )  # Here we explicitly reference 2nd  group
        + ox.literal(">")
    )

    assert s == pattern.get_group(s, 0)
    assert "EM" == pattern.get_group(s, 1)
    assert "first" == pattern.get_group(s, 2)
    assert "EM" == pattern.get_group(s, "tag")


def test_groupdict():
    s = "<EM>first</EM>"

    pattern = (
        ox.literal("<")
        + ox.group(ox.one_or_more(ox.NOT(">")), capturing=True, name="tag")
        + ox.literal(">")
        + ox.group(ox.one_or_more(ox.ANY_CHAR), capturing=True, name="content")
        + ox.literal("</")
        + ox.reference_capturing_group(
            name="tag"
        )  # Here we explicitly reference 2nd  group
        + ox.literal(">")
    )

    result = pattern.group_dict(s)
    assert len(result) == 2
    assert result["tag"] == "EM"
    assert result["content"] == "first"


def test_positive_lookahead_assertion():
    s = "something.bat"
    pattern = (
        ox.zero_or_more(ox.ANY_CHAR)
        + ox.DOT
        + ox.positive_lookahead_assertion(ox.literal("bat") + ox.END)
        + ox.zero_or_more(ox.NOT(ox.DOT))
        + ox.END
    )
    assert pattern.is_match(s)

    s = "something.exe"
    assert not pattern.is_match(s)


def test_negative_lookahead_assertion():
    s = "something.bat"
    pattern = (
        ox.zero_or_more(ox.ANY_CHAR)
        + ox.DOT
        + ox.negative_lookahead_assertion(ox.literal("bat") + ox.END)
        + ox.zero_or_more(ox.NOT(ox.DOT))
        + ox.END
    )
    assert not pattern.is_match(s)

    s = "something.exe"
    assert pattern.is_match(s)


def test_adding_regexes():
    pattern1 = ox.START
    pattern2 = ox.literal("Happy")

    pattern3 = pattern1 + pattern2
    pattern3.expr == "^Happy"

    s = "Happy Birthday"
    assert pattern3.is_match(s)


def test_splitting():
    pattern = ox.one_or_more(ox.NON_WORD)
    s = "This is a test, short and sweet, of split()."
    result = pattern.split(s)
    assert result == [
        "This",
        "is",
        "a",
        "test",
        "short",
        "and",
        "sweet",
        "of",
        "split",
        "",
    ]

    result = pattern.split(s, 3)
    assert result == ["This", "is", "a", "test, short and sweet, of split()."]


def test_capture():
    s = "<EM>first</EM>"

    pattern = (
        ox.literal("<")
        + ox.capture(ox.one_or_more(ox.NOT(">")), name="tag")
        + ox.literal(">")
        + ox.capture(ox.one_or_more(ox.ANY_CHAR))
        + ox.literal("</")
        + ox.reference_capturing_group()
        + ox.literal(">")
    )

    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")

    assert pattern.group_dict(s) == {"tag": "EM"}
