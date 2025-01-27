from dataclasses import dataclass
from typing import Iterable, Iterator, Self, Sequence, Sized, override

from pysh.core.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class Nary[
    Result,
    ChildResult,
    ChildParser: Parser = Parser[ChildResult],
](Parser[Result], Sized, Iterable[ChildParser]):
    children: Sequence[ChildParser]

    def _str_join(self, depth: int, sep: str) -> str:
        s = sep.join(child._str(depth + 1) for child in self)
        return f"({s})" if depth == 0 else s

    @override
    def __len__(self) -> int:
        return len(self.children)

    @override
    def __iter__(self) -> Iterator[ChildParser]:
        return iter(self.children)

    @override
    def _lexer(self) -> Lexer:
        lexer = Lexer()
        for child in self:
            lexer |= child.lexer()
        return lexer

    @classmethod
    def for_children(cls, *children: ChildParser) -> Self:
        return cls(tuple(children))

    def _apply_child(
        self, child: ChildParser, state: State
    ) -> tuple[State, ChildResult]:
        if child not in self:
            raise self._error(f"unknown chlid {child} in {self}")
        return self._try(lambda: child(state))
