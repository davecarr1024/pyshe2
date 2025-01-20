from dataclasses import dataclass
from typing import MutableSequence, override

from pysh.core.regex.nary import Nary
from pysh.core.regex.regex import Regex
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


@dataclass(frozen=True)
class Or(Nary):
    @override
    def _str(self, depth: int) -> str:
        s = "|".join(child._str(depth + 1) for child in self)
        if depth == 0:
            return s
        else:
            return f"({s})"

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        errors: MutableSequence[Regex.Error] = []
        for child in self:
            try:
                return child._apply(state)
            except Regex.Error as error:
                errors.append(error)
        raise self._error(None, *errors)

    @override
    def __or__(self, rhs: Regex) -> Regex:
        match rhs:
            case Or():
                return self.for_children(*self, *rhs)
            case Regex():
                return self.for_children(*self, rhs)
