from dataclasses import dataclass
from typing import Never, Optional

import pytest
from pysh.core.errors import *


@dataclass
class _PositiveInt(Errorable):
    _value: int = 0

    def __post_init__(self) -> None:
        self._assert_positive()

    def _assert_positive(self) -> None:
        if self._value < 0:
            raise self._error(f"negative value {self._value}")

    def raise_(self, msg: Optional[str] = None, *children: Error) -> Never:
        raise self._error(msg, *children)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value
        self._assert_positive()

    def set_and_get(self, value: int) -> int:
        def impl() -> int:
            self.value = value
            return self.value

        return self._try(impl, "set_and_get")


def test_raise() -> None:
    pytest.raises(_PositiveInt.Error, lambda: _PositiveInt(-1))


def test_exception_value() -> None:
    i = _PositiveInt()

    def set() -> None:
        i.value = -1

    assert pytest.raises(
        _PositiveInt.Error,
        set,
    ).value == _PositiveInt.Error(
        msg="negative value -1",
        obj=i,
    )


def test_try() -> None:
    i = _PositiveInt()
    assert pytest.raises(
        _PositiveInt.Error,
        lambda: i.set_and_get(-1),
    ).value == _PositiveInt.Error(
        msg="set_and_get",
        obj=i,
        children=[
            _PositiveInt.Error(
                msg="negative value -1",
                obj=i,
            ),
        ],
    )
