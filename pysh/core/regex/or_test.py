from typing import Optional

import pytest
from pysh.core.chars import Position
from pysh.core.regex import Or, Regex, Result, State


def test_str():
    a = Regex.literal("a")
    b = Regex.literal("b")
    c = Regex.literal("c")
    assert str(a | b | c) == "a|b|c"
    assert str(a & (b | c)) == "a(b|c)"


def test_combine(subtests):
    a = Regex.literal("a")
    b = Regex.literal("b")
    c = Regex.literal("c")
    d = Regex.literal("d")
    for regex in list[Regex](
        [
            a | b | c | d,
            (a | b) | c | d,
            a | (b | c) | d,
            a | b | (c | d),
            (a | b) | (c | d),
        ]
    ):
        with subtests.test(regex=regex):
            assert regex == Or.for_children(a, b, c, d)


def test_apply(subtests):
    for input, expected in list[tuple[str, Optional[tuple[State, Result]]]](
        [
            (
                "",
                None,
            ),
            (
                "a",
                (State(), Result.for_str("a")),
            ),
            (
                "b",
                (State(), Result.for_str("b")),
            ),
            (
                "c",
                None,
            ),
            (
                "ac",
                (State.for_str("c", Position(0, 1)), Result.for_str("a")),
            ),
            (
                "bc",
                (State.for_str("c", Position(0, 1)), Result.for_str("b")),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.literal("a") | Regex.literal("b")
            if expected is None:
                pytest.raises(Or.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
