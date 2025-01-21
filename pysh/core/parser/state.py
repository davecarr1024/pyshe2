from dataclasses import dataclass, field
from typing import Iterable, Iterator, Self, Sized, override

from pysh.core.errors import Errorable
from pysh.core.tokens import Stream, Token


@dataclass(frozen=True)
class State(Errorable, Sized, Iterable[Token]):
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

    def head(self) -> Token:
        return self._try(self.tokens.head)

    def tail(self) -> "State":
        return self.for_tokens(*self._try(self.tokens.tail))

    def empty(self) -> bool:
        return self.tokens.empty()
