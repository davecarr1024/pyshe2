from typing import Optional
import pytest
from pysh.core.chars import Position
from pysh.core.regex import Not, Regex, Result, State


def test_to_str():
    assert str(Regex.literal("a").not_()) == "^a"


def test_apply(subtests):
    regex = Regex.literal("a").not_()
    for input, expected in list[tuple[str, Optional[tuple[State, Result]]]](
        [
            (
                "a",
                None,
            ),
            (
                "b",
                (
                    State(),
                    Result.for_str("b"),
                ),
            ),
            (
                "ba",
                (
                    State.for_str("a", Position(0, 1)),
                    Result.for_str("b"),
                ),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            if expected is None:
                pytest.raises(Regex.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
