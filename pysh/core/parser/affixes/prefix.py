from dataclasses import dataclass
from typing import override

from pysh.core.parser.affixes.abstract_affixable import AbstractAffixable
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Prefix[Result](AbstractAffixable[Result], Unary[Result, Result]):
    value: Parser

    @override
    def _prefix(self) -> Parser | None:
        return self.value

    @override
    def _apply_in_affixes(self, state: State) -> tuple[State, Result]:
        return self._apply_child(state)

    @override
    def _str(self, depth: int) -> str:
        return f"{self.value} & {self.child}"
