from dataclasses import dataclass, field
from typing import Iterable, Iterator, Self, Sized, Union, overload, override

from pysh.core.tokens import Stream, Token


@dataclass(frozen=True)
class Result(Sized, Iterable[Token]):
    tokens: Stream = field(default_factory=Stream)

    @classmethod
    def for_tokens(cls, *tokens: Token) -> Self:
        return cls(Stream.for_values(*tokens))

    @override
    def __len__(self) -> int:
        return len(self.tokens)

    @override
    def __iter__(self) -> Iterator[Token]:
        return iter(self.tokens)

    @overload
    def __add__(self, rhs: "Result") -> "Result": ...

    @overload
    def __add__(self, rhs: Token) -> "Result": ...

    def __add__(self, rhs: Union["Result", Token]) -> "Result":
        match rhs:
            case Result():
                return self.for_tokens(*self, *rhs)
            case Token():
                return self.for_tokens(*self, rhs)

    def __radd__(self, lhs: Token) -> "Result":
        return self.for_tokens(lhs, *self)
