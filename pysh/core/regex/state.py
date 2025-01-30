from dataclasses import dataclass, replace
from typing import Iterable, Iterator, Optional, Self, Sized, override

from pysh.core.chars import Char, Position, Stream
from pysh.core.streams import AbstractStream


@dataclass(frozen=True)
class State(AbstractStream[Char], Sized, Iterable[Char]):
    chars: Stream

    @override
    def __len__(self) -> int:
        return len(self.chars)

    @override
    def __iter__(self) -> Iterator[Char]:
        return iter(self.chars)

    def _with_chars(self, chars: Stream) -> Self:
        return replace(self, chars=chars)

    @override
    def head(self) -> Char:
        return self.chars.head()

    @override
    def tail(self) -> Self:
        return self._with_chars(self.chars.tail())

    @classmethod
    def for_chars(cls, *chars: Char) -> Self:
        return cls(chars=Stream.for_values(*chars))

    @classmethod
    def for_str(cls, value: str, position: Optional[Position] = None) -> Self:
        return cls(chars=Stream.for_str(value, position))
