from typing import Optional

from pysh.core.chars import Char, Position, Stream


def test_for_str(subtests):
    for value, position, expected in list[tuple[str, Optional[Position], Stream]](
        [
            (
                "",
                None,
                Stream(),
            ),
            (
                "a",
                None,
                Stream(
                    [
                        Char("a"),
                    ]
                ),
            ),
            (
                "a",
                Position(1, 2),
                Stream(
                    [
                        Char("a", Position(1, 2)),
                    ]
                ),
            ),
            (
                "ab",
                None,
                Stream(
                    [
                        Char("a"),
                        Char("b", Position(0, 1)),
                    ]
                ),
            ),
            (
                "ab",
                Position(1, 2),
                Stream(
                    [
                        Char("a", Position(1, 2)),
                        Char("b", Position(1, 3)),
                    ]
                ),
            ),
            (
                "a\nb",
                None,
                Stream(
                    [
                        Char("a"),
                        Char("\n", Position(0, 1)),
                        Char("b", Position(1, 0)),
                    ]
                ),
            ),
            (
                "a\nb",
                Position(1, 2),
                Stream(
                    [
                        Char("a", Position(1, 2)),
                        Char("\n", Position(1, 3)),
                        Char("b", Position(2, 0)),
                    ]
                ),
            ),
        ]
    ):
        with subtests.test(value=value, position=position, expected=expected):
            assert Stream.for_str(value, position) == expected
