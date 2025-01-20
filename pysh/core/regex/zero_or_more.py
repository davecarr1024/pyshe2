from dataclasses import dataclass
from typing import override

from pysh.core.regex import Regex
from pysh.core.regex.result import Result
from pysh.core.regex.state import State
from pysh.core.regex.unary import Unary


@dataclass(frozen=True)
class ZeroOrMore(Unary):
    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}*"

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        result = Result()
        while True:
            try:
                state, child_result = self._apply_child(state)
                result += child_result
            except Regex.Error:
                return state, result
