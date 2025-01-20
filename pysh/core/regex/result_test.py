from typing import Iterable, Optional
import pytest
from pysh.core.chars import Char, Position, Stream
from pysh.core.regex import Result


def test_for_str():
    assert Result.for_str("a\nb", Position(1, 2)) == Result(
        Stream(
            [
                Char("a", Position(1, 2)),
                Char("\n", Position(1, 3)),
                Char("b", Position(2, 0)),
            ]
        )
    )


def test_add(subtests):
    for lhs, rhs, expected in list[tuple[Result, Result | Char, Result]](
        [
            (
                Result(),
                Result(),
                Result(),
            ),
            (
                Result.for_str("a"),
                Result(),
                Result.for_str("a"),
            ),
            (
                Result.for_str("a"),
                Result.for_str("b", Position(0, 1)),
                Result.for_str("ab"),
            ),
            (
                Result.for_str("a"),
                Char("b", Position(0, 1)),
                Result.for_str("ab"),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs + rhs == expected


def test_radd():
    assert Char("a") + Result.for_str("b", Position(0, 1)) == Result.for_str("ab")


def test_for_chars(subtests):
    for chars, expected in list[tuple[Iterable[Char], Result]](
        [
            (
                [],
                Result(),
            ),
            (
                [
                    Char("a"),
                ],
                Result.for_str("a"),
            ),
            (
                [
                    Char("a"),
                    Char("b", Position(0, 1)),
                ],
                Result.for_str("ab"),
            ),
        ]
    ):
        with subtests.test(chars=chars, expected=expected):
            assert Result.for_chars(*chars) == expected


def test_value(subtests):
    for result, expected in list[tuple[Result, str]](
        [
            (
                Result(),
                "",
            ),
            (
                Result.for_str("a"),
                "a",
            ),
            (
                Result.for_str("ab"),
                "ab",
            ),
        ]
    ):
        with subtests.test(result=result, expected=expected):
            assert result.value() == expected


def test_position(subtests):
    for result, expected in list[tuple[Result, Optional[Position]]](
        [
            (
                Result(),
                None,
            ),
            (
                Result.for_str("a"),
                Position(0, 0),
            ),
            (
                Result.for_str("ab", Position(1, 2)),
                Position(1, 2),
            ),
        ]
    ):
        with subtests.test(result=result, expected=expected):
            if expected is None:
                pytest.raises(Result.Error, result.position)
            else:
                assert result.position() == expected
