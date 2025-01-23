from dataclasses import dataclass
from typing import override

from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Suffix[Result](Unary[Result, Result]):
    value: Parser

    @override
    def _str(self, depth: int) -> str:
        return f"{self.value} & {self.child}"

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        state, result = self._apply_child(state)
        state, _ = self._try(lambda: self.value._apply(state))
        return state, result
