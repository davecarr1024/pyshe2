from dataclasses import dataclass
from typing import override

from pysh.core.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class Unary[
    Result,
    ChildResult,
    ChildParser: Parser = Parser[Result],
](Parser[Result]):
    child: ChildParser

    def _apply_child(self, state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: self.child(state))

    @override
    def _lexer(self) -> Lexer:
        return self.child.lexer()
