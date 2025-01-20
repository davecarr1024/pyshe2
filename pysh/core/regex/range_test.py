from typing import Optional
import pytest

from pysh.core.chars import Position
from pysh.core.regex import Range, Regex, Result, State


def test_invalid(subtests):
    for min, max in list[tuple[str, str]](
        [
            ("", ""),
            ("a", ""),
            ("", "b"),
            ("aa", "b"),
            ("a", "bb"),
            ("b", "a"),
        ]
    ):
        with subtests.test(min=min, max=max):
            pytest.raises(Range.Error, lambda: Regex.range(min, max))


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
                "5",
                (State(), Result.for_str("5")),
            ),
            (
                "5b",
                (State.for_str("b", Position(0, 1)), Result.for_str("5")),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.range("0", "9")
            if expected is None:
                pytest.raises(Range.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
