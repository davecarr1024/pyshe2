from dataclasses import dataclass
from typing import MutableSequence, override

from pysh.core.errors import Error
from pysh.core.parser.nary import Nary
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class Or[Result](Nary[Result, Result]):
    @override
    def _str(self, depth: int) -> str:
        return self._str_join(depth, " | ")

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        errors: MutableSequence[Error] = []
        for child in self:
            try:
                return child._apply(state)
            except Error as error:
                errors.append(error)
        raise self._error(None, *errors)

    @override
    def __or__(self, rhs: Parser[Result]) -> "Or[Result]":
        match rhs:
            case Or():
                return Or[Result].for_children(*self, *rhs)
            case Parser():
                return Or[Result].for_children(*self, rhs)
