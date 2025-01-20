from typing import Iterable
from pysh.core.lexer import Result
from pysh.core.tokens import Stream, Token


def test_for_tokens(subtests):
    for tokens, expected in list[tuple[Iterable[Token], Result]](
        [
            (
                [],
                Result(),
            ),
            (
                [
                    Token("r", "a"),
                ],
                Result(
                    Stream(
                        [
                            Token("r", "a"),
                        ]
                    )
                ),
            ),
            (
                [
                    Token("r", "a"),
                    Token("s", "b"),
                ],
                Result(
                    Stream(
                        [
                            Token("r", "a"),
                            Token("s", "b"),
                        ]
                    )
                ),
            ),
        ]
    ):
        with subtests.test(tokens=tokens, expected=expected):
            assert Result.for_tokens(*tokens) == expected


def test_add(subtests):
    for lhs, rhs, expected in list[tuple[Result, Result | Token, Result]](
        [
            (
                Result(),
                Result(),
                Result(),
            ),
            (
                Result(),
                Result.for_tokens(Token("r", "a")),
                Result.for_tokens(Token("r", "a")),
            ),
            (
                Result.for_tokens(Token("r", "a")),
                Result.for_tokens(Token("s", "b")),
                Result.for_tokens(
                    Token("r", "a"),
                    Token("s", "b"),
                ),
            ),
            (
                Result(),
                Token("r", "a"),
                Result.for_tokens(Token("r", "a")),
            ),
            (
                Result.for_tokens(Token("r", "a")),
                Token("s", "b"),
                Result.for_tokens(
                    Token("r", "a"),
                    Token("s", "b"),
                ),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs + rhs == expected


def test_radd(subtests):
    for lhs, rhs, expected in list[tuple[Token, Result, Result]](
        [
            (
                Token("r", "a"),
                Result(),
                Result.for_tokens(Token("r", "a")),
            ),
            (
                Token("r", "a"),
                Result.for_tokens(Token("s", "b")),
                Result.for_tokens(
                    Token("r", "a"),
                    Token("s", "b"),
                ),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs + rhs == expected
