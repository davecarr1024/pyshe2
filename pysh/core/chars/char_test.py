import pytest

from pysh.core.chars import Char


def test_invalid(subtests):
    for value in list[str](
        [
            "",
            "aa",
        ]
    ):
        with subtests.test(value=value):
            pytest.raises(Char.Error, lambda: Char(value))


def test_valid():
    Char("a")
