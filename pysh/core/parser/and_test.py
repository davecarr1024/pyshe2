from typing import Optional, Sequence

import pytest
from pysh.core import regex
from pysh.core.chars import Position
from pysh.core.parser import And, Parser, State
from pysh.core.tokens import Token


def test_combine(subtests):
    a = Parser.head("a")
    b = Parser.head("b")
    c = Parser.head("c")
    d = Parser.head("d")
    for parser in list[And](
        [
            a & b & c & d,
            (a & b) & c & d,
            a & (b & c) & d,
            a & b & (c & d),
            (a & b) & (c & d),
        ]
    ):
        with subtests.test(parser=parser):
            assert parser == And.for_children(a, b, c, d)


def test_apply(subtests):
    for state, expected in list[
        tuple[str | regex.State | State, Optional[tuple[State, Sequence[Token]]]]
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
                None,
            ),
            (
                "ab",
                (
                    State(),
                    [
                        Token("a", "a"),
                        Token("b", "b", Position(0, 1)),
                    ],
                ),
            ),
            (
                "aba",
                (
                    State.for_tokens(
                        Token("a", "a", Position(0, 2)),
                    ),
                    [
                        Token("a", "a"),
                        Token("b", "b", Position(0, 1)),
                    ],
                ),
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            parser = Parser.head("a") & Parser.head("b")
            if expected is None:
                pytest.raises(Parser.Error, lambda: parser(state))
            else:
                assert parser(state) == expected


def test_prefix():
    assert ("a" & (Parser.head("b").value() & Parser.head("c").value()))("abc") == (
        State(),
        ["b", "c"],
    )


def test_suffix():
    assert ((Parser.head("b").value() & Parser.head("c").value()) & "a")("bca") == (
        State(),
        ["b", "c"],
    )
