from dataclasses import dataclass
from typing import override

from pysh.core.lexer import Lexer
from pysh.core.parser.state import State
from pysh.core.parser.transform import Transform


@dataclass(frozen=True)
class WithLexer[Result](Transform[Result, Result]):
    value: Lexer

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.with_lexer({self._lexer})"

    @override
    def _lexer(self) -> Lexer:
        return self.value | super()._lexer()

    @override
    def _transform(self, child_result: Result) -> Result:
        return child_result
