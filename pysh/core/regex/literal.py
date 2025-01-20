from dataclasses import dataclass
from typing import override

from pysh.core.chars.char import Char
from pysh.core.regex.head import Head


@dataclass(frozen=True)
class Literal(Head):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) != 1:
            raise self._error(f"invalid value {repr(self.value)}")

    @override
    def _str(self, depth: int) -> str:
        return self.value

    @override
    def _apply_head(self, head: Char) -> Char:
        if head.value != self.value:
            raise self._error(f"expected {self.value} but got {head}")
        return head
