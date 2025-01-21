from dataclasses import dataclass
from typing import override

from pysh.core.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class Unary[Result, ChildResult](Parser[Result]):
    child: Parser[ChildResult]

    def _apply_child(self, state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: self.child._apply(state))

    @override
    def lexer(self) -> Lexer:
        return self.child.lexer()
