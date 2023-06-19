# pylint: skip-file
# flake8: noqa

import re
from regex import Ox
import pytest


def test_constants_can_be_found():

    s = "foo123bar"

    pattern = Ox().DIGIT.DIGIT.DIGIT.compile()

    result = re.search(pattern, s)
    assert result is not None

    results = re.findall(pattern, s)
    assert len(results) == 1
    assert results[0] == "123"


def test_starts_with():

    s = "foo123bar"

    pattern = Ox().starts_with("f").compile()
    result = re.search(pattern, s)
    assert result is not None

    pattern2 = Ox().starts_with("b").compile()
    result = re.search(pattern2, s)
    assert result is None


def test_ends_with():

    s = "foo123bar"

    pattern = Ox().ends_with("r").compile()
    result = re.search(pattern, s)
    assert result is not None

    pattern2 = Ox().starts_with("o").compile()
    result = re.search(pattern2, s)
    assert result is None


def test_is_match():
    s = "foo123bar"
    assert Ox().ends_with("r").is_match(s)
    assert not Ox().ends_with("o").is_match(s)


def test_findall():
    s = "foo123bar345"
    results = Ox().DIGIT.DIGIT.DIGIT.findall(s)
    assert len(results) == 2
    assert results[0] == "123"
    assert results[1] == "345"


def test_repeat_on_string():
    s = "foo111bar"
    assert Ox().repeat("1", 3).is_match(s)
    s = "foo123bar"
    assert not Ox().repeat("1", 3).is_match(s)


def test_repeat_on_pattern():
    s = "foo123bar"
    assert Ox().repeat(Ox().DIGIT, 3).is_match(s)

    s = "foo12bar"
    assert not Ox().repeat(Ox().DIGIT, 3).is_match(s)


def test_one_or_more_str():
    s = "foo123bar"
    pattern = Ox().one_or_more(Ox().repeated(Ox().DIGIT, 3))

    assert pattern.is_match(s)

    s = "foo123456bar"
    assert pattern.is_match(s)

    s = "foo12bar"
    assert not pattern.is_match(s)


def test_one_or_more_pattern():
    s = "foo123bar"
    assert Ox().one_or_more(Ox().DIGIT.DIGIT.DIGIT).is_match(s)

    s = "foo12bar"
    assert not Ox().one_or_more(Ox().DIGIT.DIGIT.DIGIT).is_match(s)


def test_one_or_more_laziness():
    s = "<EM>first</EM>"
    pattern = Ox().group(Ox().literal("<").one_or_more(Ox().ANY_CHAR).literal(">"))
    results = pattern.findall(s)
    assert results[0] == "<EM>first</EM>"

    pattern = Ox().group(
        Ox().literal("<").one_or_more(Ox().ANY_CHAR, lazy=True).literal(">")
    )
    results = pattern.findall(s)
    assert len(results) == 2
    assert results[0] == "<EM>"
    assert results[1] == "</EM>"


def test_blank():
    s = "foo123bar"
    assert not Ox().BLANK.is_match(s)

    s = "foo 123bar"
    assert Ox().BLANK.is_match(s)

    s = "foo    123bar"
    assert Ox().BLANK.is_match(s)


def test_n_or_more_string():
    s = "foo123bar"
    assert Ox().n_or_more("o", min=2).is_match(s)

    s = "foo123bar"
    assert not Ox().n_or_more("o", min=3).is_match(s)

    s = "foooo123bar"
    assert Ox().n_or_more("o", min=1, max=4).is_match(s)

    s = "foooo0123bar"
    assert not Ox().n_or_more("o", min=6, max=7).is_match(s)


def test_n_or_more_digit():
    s = "foo123bar"
    assert Ox().n_or_more(Ox().DIGIT, min=2).is_match(s)

    s = "foo123bar"
    assert not Ox().n_or_more(Ox().DIGIT, min=4).is_match(s)

    s = "foooo123bar"
    assert Ox().n_or_more(Ox().DIGIT, min=1, max=4).is_match(s)

    s = "foooo0123bar"
    assert not Ox().n_or_more(Ox().DIGIT, min=6, max=7).is_match(s)


def test_word():
    s = " word "
    assert Ox().WORD.is_match(s)

    results = Ox().WORD.findall(s)
    assert len(results) == 1
    assert results[0] == "word"

    s = " word test"
    results = Ox().WORD.findall(s)
    assert len(results) == 2
    assert results[0] == "word"
    assert results[1] == "test"


def test_literal():
    s = "about cats and dogs"
    assert Ox().literal("cat").is_match(s)

    assert not Ox().literal("rat").is_match(s)


def test_literal_takes_regex():
    s = "This is 1999"
    assert Ox().literal("[1-9]").repeat(Ox().literal("[0-9]"), 3).is_match(s)


def test_or():
    s = "the cat in in the house"

    assert Ox().orex_or("cat", "dog").is_match(s)
    assert Ox().orex_or(Ox().literal("cat"), Ox().literal("dog")).is_match(s)

    s = "the dog in in the house"
    assert Ox().orex_or("cat", "dog").is_match(s)

    s = "the rat in in the house"
    assert not Ox().orex_or("cat", "dog").is_match(s)


def test_optional():

    s = "We meet in February!"

    pattern = Ox().literal("Feb").optional("ruary")
    assert pattern.is_match(s)

    s = "We meet on Feb 19th!"
    assert pattern.is_match(s)

    s = "We dont meet in March!"
    assert not pattern.is_match(s)

    s = "We dont meet in a B ruary!"
    assert not pattern.is_match(s)


def test_optional_laziness():
    s = "We meet in February!"

    pattern = Ox().group(
        Ox().literal("Feb").optional("ruary", capturing=True), capturing=True
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert ("February", "ruary") in results

    pattern = Ox().group(
        Ox().literal("Feb").optional("ruary", lazy=True, capturing=True), capturing=True
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert ("Feb", "") in results


def test_not_pattern():
    s = '"string one" and "string two"'
    pattern = (
        Ox()
        .literal('"')
        .zero_or_more(Ox().contains_not(Ox().RETURN.QUOTAtION.NEWLINE), capturing=False)
        .literal('"')
    )
    results = pattern.findall(s)
    assert len(results) == 2
    assert results[0] == '"string one"'
    assert results[1] == '"string two"'


def test_capturing_in_optional():
    s = "SetValue"
    results = Ox().literal("Set").optional("Value").findall(s)
    assert results[0] == "SetValue"

    results = Ox().literal("Set").optional("Value", capturing=False).findall(s)
    assert results[0] == "SetValue"

    results = Ox().literal("Set").optional("Value", capturing=True).findall(s)
    assert results[0] == "Value"


def test_orex_and():
    s = "foo123bar"
    assert Ox().orex_and("foo", "bar").is_match(s)
    assert Ox().orex_and("foo", Ox().literal("bar"))
    assert Ox().orex_and("foo", Ox().orex_and("bar"))
    assert Ox().orex_and("foo", "bar").orex_and("123").is_match(s)
    assert Ox().orex_and("foo", "bar", "123").is_match(s)
    assert Ox().orex_and("123", "bar", "foo").is_match(s)
    assert not Ox().orex_and("foo", "baz").is_match(s)
    assert not Ox().orex_and("qux", "bar", "foo").is_match(s)


def test_orex_or():
    s = "foo123bar"
    assert Ox().orex_or("foo", Ox().literal("baz")).is_match(s)
    assert Ox().orex_or("foo", Ox().orex_or("baz")).is_match(s)
    assert Ox().orex_or("foo", "baz").is_match(s)
    assert Ox().orex_or("baz", "foo").is_match(s)
    assert Ox().orex_or("baz", "qux", "123").is_match(s)
    assert Ox().orex_or("123", "qux", "baz").is_match(s)


def test_back_reference():
    s = "<EM>first</EM>"

    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True)
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True)
        .literal("</")
        .reference_capturing_group()
        .literal(">")
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")

    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True)
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True)
        .literal("</")
        .reference_capturing_group(1)
        .literal(">")
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")

    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True)
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True)
        .literal("</")
        .reference_capturing_group(2)
        .literal(">")
    )
    assert not pattern.is_match(s)

    s = "<EM>first</first>"
    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True)
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True)
        .literal("</")
        .reference_capturing_group(2)
        .literal(">")
    )
    assert pattern.is_match(s)


def test_named_back_reference():
    s = "<EM>first</EM>"

    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True, name="tag")
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True)
        .literal("</")
        .reference_capturing_group(name="tag")
        .literal(">")
    )
    results = pattern.findall(s)
    assert len(results) == 1
    assert results[0] == ("EM", "first")


def test_optional_special_case():
    s = "b"
    # (q?)b\1 does typically not match as the empty group does not back reference
    pattern = (
        Ox().optional("q", capturing=True).literal("b").reference_capturing_group()
    )
    assert not pattern.is_match(s)
    # (q)?b\1 does typically match
    pattern = (
        Ox()
        .group(Ox().literal("q?"), capturing=True)
        .literal("b")
        .reference_capturing_group()
    )
    assert pattern.is_match(s)
    pattern = (
        Ox()
        .group(Ox().optional("q", capturing=False), capturing=True)
        .literal("b")
        .reference_capturing_group()
    )
    assert pattern.is_match(s)


def test_forward_referencing_does_not_work_in_python():
    s = "oneonetwo"
    pattern = Ox().one_or_more(
        Ox().orex_or(
            Ox().reference_capturing_group(2).literal("two"),
            Ox().group(Ox().literal("one"), capturing=True),
        ),
        capturing=True,
    )

    try:
        pattern.is_match(s)
    except:
        assert True


def test_character_class():

    s = "This costs 12$"

    pattern = Ox().repeat(Ox().DIGIT, 2).literal("$")
    # the $ is interpreted as meaning end of string
    assert not pattern.is_match(s)

    pattern = Ox().repeat(Ox().DIGIT, 2).character_class("$")
    assert pattern.is_match(s)


def test_backslash():
    s = r"this is a \string in latex"
    pattern = Ox().BACKSLASH.literal("string")
    assert pattern.is_match(s)


def test_match_new_line():
    s = """This has a
    new line"""

    assert Ox().NEWLINE.is_match(s)


def test_find_iter():
    s = "12 drummers drumming, 11 pipers piping, 10 lords a-leaping"
    iterator = Ox().DIGIT.DIGIT.finditer(s)

    counter = 0
    for match in iterator:
        assert int(match.group()) > 9
        counter += 1
    assert counter == 3


def test_replacement():
    s = "12 drummers drumming, 11 pipers piping, 10 lords a-leaping"
    pattern = Ox().DIGIT.DIGIT

    result = pattern.sub(s, "aa")
    assert result == "aa drummers drumming, aa pipers piping, aa lords a-leaping"
    # The original string is not altered
    assert s == "12 drummers drumming, 11 pipers piping, 10 lords a-leaping"


def test_compilation():
    import re

    s = " test "
    s_alt = " TEST "
    pattern = Ox().literal("test").compile()
    assert re.search(pattern, s)
    assert not re.search(pattern, s_alt)

    pattern = Ox().literal("test").compile(ignorecase=True)
    assert re.search(pattern, s)
    assert re.search(pattern, s_alt)


def test_named_groups():
    s = "<EM>first</EM>"

    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True, name="tag")
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True)
        .literal("</")
        .reference_capturing_group(name="tag")
        .literal(">")
    )

    assert s == pattern.get_group(s, 0)
    assert "EM" == pattern.get_group(s, 1)
    assert "first" == pattern.get_group(s, 2)
    assert "EM" == pattern.get_group(s, "tag")


def test_groupdict():
    s = "<EM>first</EM>"

    pattern = (
        Ox()
        .literal("<")
        .group(Ox().one_or_more(Ox().contains_not(">")), capturing=True, name="tag")
        .literal(">")
        .group(Ox().one_or_more(Ox().ANY_CHAR), capturing=True, name="content")
        .literal("</")
        .reference_capturing_group(name="tag")
        .literal(">")
    )

    result = pattern.group_dict(s)
    assert len(result) == 2
    assert result["tag"] == "EM"
    assert result["content"] == "first"


def test_positive_lookahead_assertion():
    s = "something.bat"
    pattern = (
        Ox()
        .zero_or_more(Ox().ANY_CHAR.DOT)
        .positive_lookahead_assertion(Ox().literal("bat").END)
        .zero_or_more(Ox().contains_not(Ox().DOT))
        .END
    )
    assert pattern.is_match(s)

    s = "something.exe"
    assert not pattern.is_match(s)


def test_negative_lookahead_assertion():
    s = "something.bat"
    pattern = (
        Ox()
        .one_or_more(Ox().ANY_CHAR)
        .DOT.negative_lookahead_assertion(Ox().literal("bat").END)
        .one_or_more(Ox().ANY_CHAR)
        .END
    )
    assert not pattern.is_match(s)

    s = "something.exe"
    assert pattern.is_match(s)
