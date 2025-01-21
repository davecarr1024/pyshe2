from dataclasses import dataclass, field
from typing import Iterable, Iterator, Self, Sequence, Sized, override

from pysh.core.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class Nary[Result, ChildResult](Parser[Result], Sized, Iterable[Parser[ChildResult]]):
    children: Sequence[Parser[ChildResult]]

    def _str_join(self, depth: int, sep: str) -> str:
        s = sep.join(child._str(depth + 1) for child in self)
        return f"({s})" if depth == 0 else s

    @override
    def __len__(self) -> int:
        return len(list(self.children))

    @override
    def __iter__(self) -> Iterator[Parser[ChildResult]]:
        return iter(self.children)

    @override
    def lexer(self) -> Lexer:
        lexer = Lexer()
        for child in self:
            lexer |= child.lexer()
        return lexer

    @classmethod
    def for_children(cls, *children: Parser[ChildResult]) -> Self:
        return cls(list(children))

    def _apply_child(
        self, child: Parser[ChildResult], state: State
    ) -> tuple[State, ChildResult]:
        if child not in self:
            raise self._error(f"unknown chlid {child} in {self}")
        return self._try(lambda: child._apply(state))
