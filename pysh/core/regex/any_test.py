from typing import Optional

import pytest

from pysh.core.chars import Position
from pysh.core.regex import Any, Result, State
from pysh.core.regex.regex import Regex


def test_apply(subtests):
    for input, expected in list[tuple[str, Optional[tuple[State, Result]]]](
        [
            (
                "",
                None,
            ),
            (
                "a",
                (
                    State(),
                    Result.for_str("a"),
                ),
            ),
            (
                "ab",
                (
                    State.for_str("b", Position(0, 1)),
                    Result.for_str("a"),
                ),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            regex = Regex.any()
            if expected is None:
                pytest.raises(Any.Error, lambda: regex(input))
            else:
                assert regex(input) == expected
