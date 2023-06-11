# pylint: skip-file
# flake8: noqa

import re
from regex import Orex
import pytest


def test_constants_can_be_found():

    s = "foo123bar"

    orex = Orex()
    pattern = orex.DIGIT.DIGIT.DIGIT.compile()

    result = re.search(pattern, s)
    assert result is not None

    results = re.findall(pattern, s)
    assert len(results) == 1
    assert results[0] == "123"
