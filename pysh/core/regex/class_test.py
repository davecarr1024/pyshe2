from typing import Optional

import pytest
from pysh.core.chars import Position
from pysh.core.regex import Class, Regex, Result, State


def test_str(subtests):
    for class_, expected in list[tuple[Regex, str]](
        [
            (
                Regex.class_(""),
                "[]",
            ),
            (
                Regex.class_("abc"),
                "[abc]",
            ),
            (
                Regex.class_("abc", "d"),
                "d",
            ),
            (
                Regex.digits(),
                r"\d",
            ),
            (
                Regex.whitespace(),
                r"\w",
            ),
        ]
    ):
        with subtests.test(class_=class_, expected=expected):
            assert str(class_) == expected


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
                "ab",
                (State.for_str("b", Position(0, 1)), Result.for_str("a")),
            ),
            (
                "c",
                None,
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.class_("ab")
            if expected is None:
                pytest.raises(Class.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
