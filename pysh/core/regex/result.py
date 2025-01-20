from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Self, Sized, Union, overload, override

from pysh.core.chars import Char, Position, Stream
from pysh.core.errors import Errorable


@dataclass(frozen=True)
class Result(Errorable, Sized, Iterable[Char]):
    chars: Stream = field(default_factory=Stream)

    @override
    def __len__(self) -> int:
        return len(self.chars)

    @override
    def __iter__(self) -> Iterator[Char]:
        return iter(self.chars)

    def _with_chars(self, chars: Stream) -> Self:
        return self.__class__(chars)

    @overload
    def __add__(self, rhs: Char) -> Self: ...

    @overload
    def __add__(self, rhs: "Result") -> Self: ...

    def __add__(self, rhs: Union[Char, "Result"]) -> Self:
        match rhs:
            case Result():
                return self._with_chars(self.chars + rhs.chars)
            case _:
                return self._with_chars(self.chars + rhs)

    def __radd__(self, lhs: Char) -> Self:
        return self._with_chars(lhs + self.chars)

    @classmethod
    def for_str(cls, input: str, position: Optional[Position] = None) -> Self:
        return cls(Stream.for_str(input, position))

    @classmethod
    def for_chars(cls, *chars: Char) -> Self:
        return cls()._with_chars(Stream.for_values(*chars))

    def value(self) -> str:
        return "".join(char.value for char in self)

    def head(self) -> Char:
        return self._try(
            lambda: self.chars.head(),
            "failed to get head of regex result",
        )

    def position(self) -> Position:
        return self.head().position
