from dataclasses import dataclass
from typing import override

from pysh.core.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Prefix[Result](Unary[Result, Result]):
    value: Parser

    @override
    def _str(self, depth: int) -> str:
        return f"{self.value} & {self.child}"

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        state, _ = self._try(lambda: self.value._apply(state))
        return self._apply_child(state)

    @override
    def lexer(self) -> Lexer:
        return self.value.lexer() | super().lexer()
