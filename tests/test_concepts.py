# pylint: skip-file
# flake8: noqa

import re
from regex import Orex
import pytest


def test_constants_can_be_found():

    s = "foo123bar"

    pattern = Orex().DIGIT.DIGIT.DIGIT.compile()

    result = re.search(pattern, s)
    assert result is not None

    results = re.findall(pattern, s)
    assert len(results) == 1
    assert results[0] == "123"


def test_starts_with():

    s = "foo123bar"

    pattern = Orex().starts_with("f").compile()
    result = re.search(pattern, s)
    assert result is not None

    pattern2 = Orex().starts_with("b").compile()
    result = re.search(pattern2, s)
    assert result is None


def test_ends_with():

    s = "foo123bar"

    pattern = Orex().ends_with("r").compile()
    result = re.search(pattern, s)
    assert result is not None

    pattern2 = Orex().starts_with("o").compile()
    result = re.search(pattern2, s)
    assert result is None


def test_is_match():
    s = "foo123bar"
    assert Orex().ends_with("r").is_match(s)
    assert not Orex().ends_with("o").is_match(s)


def test_find_instances():
    s = "foo123bar345"
    results = Orex().DIGIT.DIGIT.DIGIT.find_instances(s)
    assert len(results) == 2
    assert results[0] == "123"
    assert results[1] == "345"


def test_repeat_on_string():
    s = "foo111bar"
    assert Orex().repeat("1", 3).is_match(s)
    s = "foo123bar"
    assert not Orex().repeat("1", 3).is_match(s)


def test_repeat_on_pattern():
    s = "foo123bar"
    assert Orex().repeat(Orex().DIGIT, 3).is_match(s)

    s = "foo12bar"
    assert not Orex().repeat(Orex().DIGIT, 3).is_match(s)


def test_one_or_more_str():
    s = "foo123bar"
    pattern = Orex().one_or_more(Orex().repeated(Orex().DIGIT, 3))

    assert pattern.is_match(s)

    s = "foo123456bar"
    assert pattern.is_match(s)

    s = "foo12bar"
    assert not pattern.is_match(s)


def test_one_or_more_pattern():
    s = "foo123bar"
    assert Orex().one_or_more(Orex().DIGIT.DIGIT.DIGIT).is_match(s)

    s = "foo12bar"
    assert not Orex().one_or_more(Orex().DIGIT.DIGIT.DIGIT).is_match(s)


def test_blank():
    s = "foo123bar"
    assert not Orex().BLANK.is_match(s)

    s = "foo 123bar"
    assert Orex().BLANK.is_match(s)

    s = "foo    123bar"
    assert Orex().BLANK.is_match(s)


def test_n_or_more_string():
    s = "foo123bar"
    assert Orex().n_or_more("o", min=2).is_match(s)

    s = "foo123bar"
    assert not Orex().n_or_more("o", min=3).is_match(s)

    s = "foooo123bar"
    assert Orex().n_or_more("o", min=1, max=4).is_match(s)

    s = "foooo0123bar"
    assert not Orex().n_or_more("o", min=6, max=7).is_match(s)


def test_n_or_more_digit():
    s = "foo123bar"
    assert Orex().n_or_more(Orex().DIGIT, min=2).is_match(s)

    s = "foo123bar"
    assert not Orex().n_or_more(Orex().DIGIT, min=4).is_match(s)

    s = "foooo123bar"
    assert Orex().n_or_more(Orex().DIGIT, min=1, max=4).is_match(s)

    s = "foooo0123bar"
    assert not Orex().n_or_more(Orex().DIGIT, min=6, max=7).is_match(s)


def test_word():
    s = " word "
    assert Orex().WORD.is_match(s)

    results = Orex().WORD.find_instances(s)
    assert len(results) == 1
    assert results[0] == "word"

    s = " word test"
    results = Orex().WORD.find_instances(s)
    assert len(results) == 2
    assert results[0] == "word"
    assert results[1] == "test"


def test_literal():
    s = "about cats and dogs"
    assert Orex().literal("cat").is_match(s)

    assert not Orex().literal("rat").is_match(s)


def test_or():
    s = "the cat in in the house"

    assert Orex().orex_or("cat", "dog").is_match(s)
    assert Orex().orex_or(Orex().literal("cat"), Orex().literal("dog")).is_match(s)

    s = "the dog in in the house"
    assert Orex().orex_or("cat", "dog").is_match(s)

    s = "the rat in in the house"
    assert not Orex().orex_or("cat", "dog").is_match(s)


def test_optional():

    s = "We meet in February!"

    pattern = Orex().literal("Feb").optional("ruary")
    assert pattern.is_match(s)

    s = "We meet on Feb 19th!"
    assert pattern.is_match(s)

    s = "We dont meet in March!"
    assert not pattern.is_match(s)

    s = "We dont meet in a B ruary!"
    assert not pattern.is_match(s)


def test_optional_laziness():
    s = "We meet in February!"

    pattern = Orex().group(Orex().literal("Feb").optional("ruary"))
    results = pattern.find_instances(s)
    assert len(results) == 1
    assert ("February", "ruary") in results

    pattern = Orex().group(Orex().literal("Feb").optional("ruary", lazy=True))
    results = pattern.find_instances(s)
    assert len(results) == 1
    assert ("Feb", "") in results


def test_not_pattern():
    s = '"string one" and "string two"'
    pattern = (
        Orex()
        .literal('"')
        .zero_or_more(Orex().orex_not(Orex().literal('"')))
        .literal('"')
    )
    pattern.compile()
