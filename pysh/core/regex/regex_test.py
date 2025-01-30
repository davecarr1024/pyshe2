from typing import Optional

import pytest

from pysh.core.errors import Error
from pysh.core.regex import And, Regex


def test_for_str(subtests):
    for input, expected in list[tuple[str, Optional[Regex]]](
        [
            (
                "",
                None,
            ),
            (
                "a",
                Regex.literal("a"),
            ),
            (
                "ab",
                Regex.literal("a") & Regex.literal("b"),
            ),
            (
                "[",
                None,
            ),
            (
                "[a",
                None,
            ),
            (
                "[a-",
                None,
            ),
            (
                "[a-z",
                None,
            ),
            (
                "[a-z]",
                Regex.range("a", "z"),
            ),
            (
                "[a-z]b",
                Regex.range("a", "z") & Regex.literal("b"),
            ),
            (
                "a*",
                Regex.literal("a").zero_or_more(),
            ),
            (
                "a*b",
                Regex.literal("a").zero_or_more() & Regex.literal("b"),
            ),
            (
                "a+",
                Regex.literal("a").one_or_more(),
            ),
            (
                "a+b",
                Regex.literal("a").one_or_more() & Regex.literal("b"),
            ),
            (
                "a?",
                Regex.literal("a").zero_or_one(),
            ),
            (
                "a?b",
                Regex.literal("a").zero_or_one() & Regex.literal("b"),
            ),
            (
                '(a)',
                Regex.literal('a'),
            ),
            (
                '(ab)',
                Regex.literal('a') & Regex.literal('b'),
            ),
            (
                '((ab))',
                Regex.literal('a') & Regex.literal('b'),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            if expected is None:
                pytest.raises(Regex.ParseError, lambda: Regex.for_str(input))
            else:
                assert Regex.for_str(input) == expected
