from dataclasses import dataclass, field, replace
from typing import Iterable, Iterator, Optional, Self, Sequence, Sized, override

from pysh.core.chars import Char, Position, Stream
from pysh.core.processor.transform import AbstractTransform
from pysh.core.regex.state import State
from pysh.core.streams import AbstractStream


@dataclass(frozen=True)
class Result(AbstractStream[Char], Sized, Iterable[Char]):
    chars: Stream = field(default_factory=Stream)

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

    def __add__(self, rhs: Char | Self) -> Self:
        match rhs:
            case Char():
                return self._with_chars(self.chars + rhs)
            case Result():
                return self._with_chars(self.chars + rhs.chars)

    def __radd__(self, lhs: Char) -> Self:
        return self._with_chars(lhs + self.chars)

    @classmethod
    def merge(cls, *results: Self) -> Self:
        result = cls()
        for value in results:
            result += value
        return result

    @dataclass(frozen=True)
    class Merger(AbstractTransform[State, "Result", Sequence["Result"]]):
        @override
        def _transform(self, result: Sequence["Result"]) -> "Result":
            return Result.merge(*result)

        @override
        def _str(self, depth: int) -> str:
            return "regex.Result.Merger()"
