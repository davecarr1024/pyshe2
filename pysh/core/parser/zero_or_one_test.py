from typing import Optional
import pytest
from pysh.core.chars import Position
from pysh.core.lexer import Rule
from pysh.core.parser import Parser, State
from pysh.core.tokens import Token


def test_str():
    assert str(Parser.head("a").zero_or_one()) == "a?"


def test_apply(subtests):
    parser = Parser.head("a").value().zero_or_one().with_lexer(Rule.for_str("b"))
    for input, expected in list[tuple[str, Optional[tuple[State, Optional[str]]]]](
        [
            (
                "",
                (State(), None),
            ),
            (
                "b",
                (
                    State.for_tokens(
                        Token("b", "b"),
                    ),
                    None,
                ),
            ),
            (
                "a",
                (
                    State(),
                    "a",
                ),
            ),
            (
                "ab",
                (
                    State.for_tokens(
                        Token("b", "b", Position(0, 1)),
                    ),
                    "a",
                ),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            if expected is None:
                pytest.raises(Parser.Error, lambda: parser(input))
            else:
                assert parser(input) == expected
