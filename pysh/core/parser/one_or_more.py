from dataclasses import dataclass
from typing import MutableSequence, Sequence, override

from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class OneOrMore[
    Result,
    ChildParser: Parser = Parser,
](
    Unary[
        Sequence[Result],
        Result,
        ChildParser,
    ]
):
    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}+"

    @override
    def _apply(self, state: State) -> tuple[State, Sequence[Result]]:
        state, child_result = self._apply_child(state)
        result: MutableSequence[Result] = [child_result]
        while True:
            try:
                state, child_result = self._apply_child(state)
                result.append(child_result)
            except Parser.Error:
                return state, result
