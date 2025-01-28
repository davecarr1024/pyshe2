from dataclasses import dataclass
from typing import MutableSequence, Optional, Sequence, override

from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class ZeroOrOne[
    Result,
    ChildParser: Parser = Parser,
](
    Unary[
        Optional[Result],
        Result,
        ChildParser,
    ]
):
    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}?"

    @override
    def _apply(self, state: State) -> tuple[State, Optional[Result]]:
        try:
            return self._apply_child(state)
        except Parser.Error:
            return state, None
