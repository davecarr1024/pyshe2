from dataclasses import dataclass
from typing import override

from pysh.core.chars.char import Char
from pysh.core.errors import Error
from pysh.core.regex.head import Head
from pysh.core.regex.unary import Unary


@dataclass(frozen=True)
class Not(Unary[Head], Head):
    @override
    def _apply_head(self, head: Char) -> Char:
        try:
            head = self.child._apply_head(head)
        except Error:
            return head
        raise self._error(
            f"not successfully applied child {self.child}: got {head}"
        )

    @override
    def _str(self, depth: int) -> str:
        return f"^{self.child}"
