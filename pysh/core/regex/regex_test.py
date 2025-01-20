from typing import Optional

import pytest

from pysh.core.regex import And, Regex


def test_for_str(subtests):
    for input, expected in list[tuple[str, Optional[Regex]]](
        [
            (
                "a",
                Regex.literal("a"),
            ),
            (
                "ab",
                Regex.literal("a") & Regex.literal("b"),
            ),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            if expected is None:
                pytest.raises(Regex.Error, Regex.for_str(input))
            else:
                assert Regex.for_str(input) == expected
