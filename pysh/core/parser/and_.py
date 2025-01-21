from dataclasses import dataclass
from types import NotImplementedType
from typing import MutableSequence, Self, Sequence, Union, overload, override

from pysh.core.parser.nary import Nary
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.suffix import Suffix


@dataclass(frozen=True)
class And[Result](Nary[Sequence[Result], Result]):
    @override
    def _str(self, depth: int) -> str:
        return self._str_join(depth, " & ")

    @override
    def _apply(self, state: State) -> tuple[State, Sequence[Result]]:
        result: MutableSequence[Result] = []
        for child in self:
            state, child_result = self._apply_child(child, state)
            result.append(child_result)
        return state, result

    @override
    def __and__(  # type: ignore
        self,
        rhs: Union[
            str,
            Parser[Result],
        ],
    ) -> Parser[Sequence[Result]]:
        match rhs:
            case And():
                return And[Result].for_children(*self, *rhs)
            case Parser():
                return And[Result].for_children(*self, rhs)
            case str():
                return self.suffix(self.head(rhs))
