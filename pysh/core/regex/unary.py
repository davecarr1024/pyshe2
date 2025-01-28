from dataclasses import dataclass

from pysh.core.regex.regex import Regex
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


@dataclass(frozen=True)
class Unary[Child: Regex = Regex](Regex):
    child: Child

    def _apply_child(self, state: State) -> tuple[State, Result]:
        return self._try(lambda: self.child._apply(state))
