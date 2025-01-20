from typing import Optional
import pytest
from pysh.core.chars import Position
from pysh.core.regex import Literal, Regex, Result, State


def test_invalid(subtests):
    for value in list[str](
        [
            "",
            "aa",
        ]
    ):
        with subtests.test(value=value):
            pytest.raises(Literal.Error, lambda: Regex.literal(value))


def test_apply(subtests):
    for input, expected in list[tuple[str, Optional[tuple[State, Result]]]](
        [
            (
                "",
                None,
            ),
            (
                "a",
                (
                    State(),
                    Result.for_str("a"),
                ),
            ),
            (
                "b",
                None,
            ),
            (
                "ab",
                (
                    State.for_str("b", Position(0, 1)),
                    Result.for_str("a"),
                ),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.literal("a")
            if expected is None:
                pytest.raises(Literal.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
