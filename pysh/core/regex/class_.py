from dataclasses import dataclass
from typing import FrozenSet, Iterable, Iterator, Optional, Sized, override

from pysh.core.chars.char import Char
from pysh.core.regex.head import Head


@dataclass(frozen=True)
class Class(Head, Sized, Iterable[str]):
    values: FrozenSet[str]
    display: Optional[str] = None

    @override
    def __len__(self) -> int:
        return len(self.values)

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self.values)

    def __post_init__(self) -> None:
        if any(len(value) != 1 for value in self.values):
            raise self._error(f"invalid values {self.values}")

    @override
    def _str(self, depth: int) -> str:
        return self.display or f'[{"".join(sorted(self))}]'

    @override
    def _apply_head(self, head: Char) -> Char:
        if head.value not in self.values:
            raise self._error(f"expected values in {self} but got {head}")
        return head
