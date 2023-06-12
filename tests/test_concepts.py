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
