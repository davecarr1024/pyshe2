from typing import Optional

import pytest
from pysh.core.chars import Position
from pysh.core.lexer import Rule
from pysh.core.regex import Regex, State
from pysh.core.tokens import Token


def test_for_str(subtests):
    for name, value, expected in list[tuple[str, None | str | Regex, Rule]](
        [
            (
                "a",
                None,
                Rule("a", Regex.literal("a")),
            ),
            (
                "r",
                "a",
                Rule("r", Regex.literal("a")),
            ),
            (
                "r",
                Regex.literal("a"),
                Rule("r", Regex.literal("a")),
            ),
        ]
    ):
        with subtests.test(name=name, value=value, expected=expected):
            assert Rule.for_str(name, value) == expected


def test_apply(subtests):
    for state, expected in list[tuple[str | State, Optional[tuple[State, Token]]]](
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
                State.for_str("a", Position(1, 2)),
                (State(), Token("r", "a", Position(1, 2))),
            ),
            (
                "ab",
                (State.for_str("b", Position(0, 1)), Token("r", "a")),
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            rule = Rule.for_str("r", "a")
            if expected is None:
                pytest.raises(Rule.Error, lambda: rule(state))
            else:
                assert rule(state) == expected
