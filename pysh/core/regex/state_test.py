import pytest
from pysh.core.chars import Char, Position, Stream
from pysh.core.regex import State


def test_for_str():
    assert State.for_str("a\nb", Position(1, 2)) == State(
        Stream(
            [
                Char("a", Position(1, 2)),
                Char("\n", Position(1, 3)),
                Char("b", Position(2, 0)),
            ]
        )
    )


def test_head():
    pytest.raises(State.Error, State().head)
    assert State.for_str("a").head() == Char("a")
    assert State.for_str("ab").head() == Char("a")


def test_tail():
    pytest.raises(State.Error, State().tail)
    assert State.for_str("a").tail() == State()
    assert State.for_str("ab").tail() == State.for_str("b", Position(0, 1))
