from typing import Optional

import pytest
from pysh.core.chars import Position
from pysh.core.lexer import Lexer, Result, Rule
from pysh.core.regex import State
from pysh.core.tokens import Token


def test_or(subtests):
    a = Rule.for_str("a")
    b = Rule.for_str("b")
    for lhs, rhs, expected in list[tuple[Lexer, Lexer | Rule, Lexer]](
        [
            (
                Lexer(),
                Lexer(),
                Lexer(),
            ),
            (
                Lexer.for_rules(a),
                Lexer(),
                Lexer.for_rules(a),
            ),
            (
                Lexer.for_rules(a),
                Lexer.for_rules(b),
                Lexer.for_rules(a, b),
            ),
            (
                Lexer.for_rules(a, b),
                Lexer.for_rules(a, b),
                Lexer.for_rules(a, b),
            ),
            (
                Lexer.for_rules(a),
                b,
                Lexer.for_rules(a, b),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs | rhs == expected


def test_ror():
    a = Rule.for_str("a")
    b = Rule.for_str("b")
    assert a | Lexer.for_rules(b) == Lexer.for_rules(a, b)


def test_apply(subtests):
    for state, expected in list[tuple[str | State, Optional[Result]]](
        [
            (
                "",
                Result(),
            ),
            (
                "c",
                None,
            ),
            (
                "a",
                Result.for_tokens(
                    Token("r", "a"),
                ),
            ),
            (
                "b",
                Result.for_tokens(
                    Token("s", "b"),
                ),
            ),
            (
                "ab",
                Result.for_tokens(
                    Token("r", "a"),
                    Token("s", "b", Position(0, 1)),
                ),
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            lexer = Lexer.for_rules(
                Rule.for_str("r", "a"),
                Rule.for_str("s", "b"),
            )
            if expected is None:
                pytest.raises(Lexer.Error, lambda: lexer(state))
            else:
                assert lexer(state) == expected


def test_include():
    assert Lexer.for_rules(Rule.for_str("a"), Rule.for_str("b", include=False))(
        "ab"
    ) == Result.for_tokens(Token("a", "a"))


def test_ambiguous():
    pytest.raises(
        Lexer.Error,
        lambda: Lexer.for_rules(Rule.for_str("r", "a"), Rule.for_str("s", "a"))("a"),
    )
