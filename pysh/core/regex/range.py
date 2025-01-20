from dataclasses import dataclass
from typing import override
from pysh.core.chars.char import Char
from pysh.core.regex.head import Head


@dataclass(frozen=True)
class Range(Head):
    min: str
    max: str

    def __post_init__(self) -> None:
        if len(self.min) != 1 or len(self.max) != 1 or self.max <= self.min:
            raise self._error(f"invalid range {self.min} {self.max}")

    @override
    def _str(self, depth: int) -> str:
        return f"[{self.min}-{self.max}]"

    @override
    def _apply_head(self, head: Char) -> Char:
        if head.value > self.max or head.value < self.min:
            raise self._error(f"expected {self} but got {head}")
        return head
