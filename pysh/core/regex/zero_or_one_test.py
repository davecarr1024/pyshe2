from typing import Optional

import pytest

from pysh.core.chars import Position
from pysh.core.regex import Regex, Result, State, ZeroOrOne


def test_str():
    assert str(Regex.literal("a").zero_or_one()) == "a?"


def test_apply(subtests):
    for input, expected in list[tuple[str, Optional[tuple[State, Result]]]](
        [
            (
                "",
                (State(), Result()),
            ),
            (
                "a",
                (State(), Result.for_str("a")),
            ),
            (
                "b",
                (State.for_str("b"), Result()),
            ),
            (
                "ab",
                (State.for_str("b", Position(0, 1)), Result.for_str("a")),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.literal("a").zero_or_one()
            if expected is None:
                pytest.raises(ZeroOrOne.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
