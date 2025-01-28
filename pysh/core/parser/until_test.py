from typing import Optional, Sequence

import pytest
from pysh.core.chars import Position
from pysh.core.parser import Parser, State
from pysh.core.tokens import Token


def test_apply_until_empty(subtests):
    parser = Parser.head("a").value().until_empty()
    for input, expected in list[tuple[str, Optional[list[str]]]](
        [
            ("", []),
            ("b", None),
            ("a", ["a"]),
            ("ab", None),
            ("aa", ["a", "a"]),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            if expected is None:
                pytest.raises(Parser.Error, lambda: parser(input))
            else:
                assert parser(input) == (State(), expected)


def test_apply_until(subtests):
    parser = Parser.head("a").value().until(Parser.head("b"))
    for input, expected in list[tuple[str, Optional[tuple[State, list[str]]]]](
        [
            (
                "",
                None,
            ),
            (
                "b",
                (
                    State.for_tokens(Token("b", "b")),
                    [],
                ),
            ),
            (
                "a",
                None,
            ),
            (
                "ab",
                (
                    State.for_tokens(Token("b", "b", Position(0, 1))),
                    ["a"],
                ),
            ),
            (
                "aa",
                None,
            ),
            (
                "aab",
                (
                    State.for_tokens(Token("b", "b", Position(0, 2))),
                    ["a", "a"],
                ),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            if expected is None:
                pytest.raises(Parser.Error, lambda: parser(input))
            else:
                assert parser(input) == expected
