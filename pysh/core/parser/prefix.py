from dataclasses import dataclass
from typing import override

from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Prefix[Result](Unary[Result, Result]):
    prefix: Parser

    @override
    def _str(self, depth: int) -> str:
        return f"{self.prefix} & {self.child}"

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        state, _ = self._try(lambda: self.prefix._apply(state))
        return self._apply_child(state)
