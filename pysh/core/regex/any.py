from dataclasses import dataclass
from typing import override

from pysh.core.chars.char import Char
from pysh.core.regex.head import Head


@dataclass(frozen=True)
class Any(Head):
    @override
    def _str(self, depth: int) -> str:
        return "."

    @override
    def _apply_head(self, head: Char) -> Char:
        return head
