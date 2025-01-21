from typing import Optional

import pytest
from pysh.core import regex
from pysh.core.chars import Position
from pysh.core.lexer import Rule
from pysh.core.parser import Head, Parser, State
from pysh.core.tokens import Token


def test_for_str(subtests):
    for name, value, expected in list[tuple[str, None | str | regex.Regex, Head]](
        [
            (
                "a",
                None,
                Head(Rule("a", regex.Regex.literal("a"))),
            ),
            (
                "r",
                "a",
                Head(Rule("r", regex.Regex.literal("a"))),
            ),
            (
                "r",
                regex.Regex.literal("a"),
                Head(Rule("r", regex.Regex.literal("a"))),
            ),
        ]
    ):
        with subtests.test(name=name, value=value, expected=expected):
            assert Head.for_str(name, value) == expected


def test_str(subtests):
    for parser, expected in list[tuple[Head, str]](
        [
            (
                Head.for_str("a"),
                "a",
            ),
            (
                Head.for_str("r", "a"),
                "r(a)",
            ),
            (
                Head.for_str("r", regex.Regex.literal("a")),
                "r(a)",
            ),
        ]
    ):
        with subtests.test(parser=parser, expected=expected):
            assert str(parser) == expected


def test_apply(subtests):
    for state, expected in list[
        tuple[str | regex.State | State, Optional[tuple[State, Token]]]
    ](
        [
            (
                "",
                None,
            ),
            (
                "b",
                None,
            ),
            (
                "a",
                (State(), Token("r", "a")),
            ),
            (
                regex.State.for_str("a", Position(1, 2)),
                (State(), Token("r", "a", Position(1, 2))),
            ),
            (
                "aa",
                (
                    State.for_tokens(Token("r", "a", Position(0, 1))),
                    Token("r", "a"),
                ),
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            parser = Parser.head("r", "a")
            if expected is None:
                pytest.raises(Parser.Error, lambda: parser(state))
            else:
                assert parser(state) == expected
