from abc import ABC
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Self, Sequence, Sized, Union, overload, override

from pysh.core.errors import Errorable
from pysh.core.streams.abstract_stream import AbstractStream


@dataclass(frozen=True)
class Stream[T](Errorable, AbstractStream[T]):
    values: Sequence[T] = field(default_factory=list)

    def __str__(self) -> str:
        return str(self.values)

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> Iterator[T]:
        return iter(self.values)

    def empty(self) -> bool:
        return len(self) == 0

    def _assert_not_empty(self) -> None:
        if self.empty():
            raise self._error("empty stream")

    def head(self) -> T:
        self._assert_not_empty()
        return next(iter(self))

    def _with_values(self, values: Iterable[T]) -> Self:
        return self.__class__(list(values))

    def tail(self) -> Self:
        self._assert_not_empty()
        return self._with_values(self.values[1:])

    @overload
    def __add__(self, rhs: "Stream[T]") -> Self: ...

    @overload
    def __add__(self, rhs: T) -> Self: ...

    def __add__(self, rhs: Union["Stream[T]", T]) -> Self:
        match rhs:
            case Stream():
                return self._with_values(list(self) + list(rhs))
            case _:
                return self._with_values(list(self) + [rhs])

    def __radd__(self, lhs: T) -> Self:
        return self._with_values([lhs] + list(self))

    @classmethod
    def for_values(cls, *values: T) -> Self:
        return cls()._with_values(values)
