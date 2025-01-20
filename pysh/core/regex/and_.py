from dataclasses import dataclass
from typing import override

from pysh.core.regex.nary import Nary
from pysh.core.regex.regex import Regex
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


@dataclass(frozen=True)
class And(Nary):
    @override
    def _str(self, depth: int) -> str:
        s = f"{''.join(child._str(depth+1) for child in self)}"
        if depth == 0:
            return s
        else:
            return f"({s})"

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        result = Result()
        for child in self:
            state, child_result = self._apply_child(child, state)
            result += child_result
        return state, result

    def __and__(self, rhs: Regex) -> Regex:
        match rhs:
            case And():
                return And.for_children(*self, *rhs)
            case Regex():
                return And.for_children(*self, rhs)
