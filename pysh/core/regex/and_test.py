from typing import Optional

import pytest
from pysh.core.chars import Position
from pysh.core.regex import And, Regex, Result, State


def test_str():
    a = Regex.literal("a")
    b = Regex.literal("b")
    c = Regex.literal("c")
    assert str(a & b & c) == "abc"
    assert str(a | (b & c)) == "a|(bc)"


def test_combine(subtests):
    a = Regex.literal("a")
    b = Regex.literal("b")
    c = Regex.literal("c")
    d = Regex.literal("d")
    for regex in list[Regex](
        [
            a & b & c & d,
            (a & b) & c & d,
            a & (b & c) & d,
            a & b & (c & d),
            (a & b) & (c & d),
        ]
    ):
        with subtests.test(regex=regex):
            assert regex == And.for_children(a, b, c, d)


def test_apply(subtests):
    for input, expected in list[tuple[str, Optional[tuple[State, Result]]]](
        [
            (
                "",
                None,
            ),
            (
                "a",
                None,
            ),
            (
                "b",
                None,
            ),
            (
                "ab",
                (State(), Result.for_str("ab")),
            ),
            (
                "abc",
                (State.for_str("c", Position(0, 2)), Result.for_str("ab")),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.literal("a") & Regex.literal("b")
            if expected is None:
                pytest.raises(And.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
