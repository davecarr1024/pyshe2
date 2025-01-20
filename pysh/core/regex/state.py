from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Self, Sized, override

from pysh.core.chars import Char, Position, Stream
from pysh.core.errors import Errorable


@dataclass(frozen=True)
class State(Errorable, Sized, Iterable[Char]):
    chars: Stream = field(default_factory=Stream)

    @override
    def __len__(self) -> int:
        return len(self.chars)

    @override
    def __iter__(self) -> Iterator[Char]:
        return iter(self.chars)

    @classmethod
    def for_str(
        cls,
        input: str,
        position: Optional[Position] = None,
    ) -> "State":
        return cls(Stream.for_str(input, position))

    def head(self) -> Char:
        return self._try(self.chars.head)

    def _with_chars(self, chars: Stream) -> Self:
        return self.__class__(chars)

    def tail(self) -> Self:
        return self._with_chars(self._try(self.chars.tail))

    def empty(self) -> bool:
        return self.chars.empty()
