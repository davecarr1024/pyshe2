from dataclasses import dataclass
from typing import override

from pysh.core.lexer import Lexer
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class WithLexer[Result](Unary[Result, Result]):
    _lexer: Lexer

    @override
    def _str(self, depth:int)->str:
        return f"{self.child}.with_lexer({self._lexer})"

    @override
    def lexer(self) -> Lexer:
        return self._lexer | super().lexer()

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        return self._apply_child(state)
