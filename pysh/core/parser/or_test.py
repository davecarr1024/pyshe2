from typing import Optional, Sequence

import pytest
from pysh.core import regex
from pysh.core.chars import Position
from pysh.core.lexer import Lexer, Rule
from pysh.core.parser import Or, Parser, State
from pysh.core.tokens import Token


def test_combine(subtests):
    a = Parser.head("a")
    b = Parser.head("b")
    c = Parser.head("c")
    d = Parser.head("d")
    for parser in list[Or](
        [
            a | b | c | d,
            (a | b) | c | d,
            a | (b | c) | d,
            a | b | (c | d),
            (a | b) | (c | d),
        ]
    ):
        with subtests.test(parser=parser):
            assert parser == Or.for_children(a, b, c, d)


def test_apply(subtests):
    for state, expected in list[
        tuple[str | regex.State | State, Optional[tuple[State, str]]]
    ](
        [
            (
                "",
                None,
            ),
            (
                "a",
                (State(), "a"),
            ),
            (
                "b",
                (State(), "b"),
            ),
            (
                "c",
                None,
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            parser: Parser[str] = (
                Parser.head("a").value() | Parser.head("b").value()
            ).with_lexer(Lexer.for_rules(Rule.for_str("c")))
            if expected is None:
                pytest.raises(Parser.Error, lambda: parser(state))
            else:
                assert parser(state) == expected
