from dataclasses import dataclass, field
from typing import Iterable, Iterator, Self, Sequence, Sized, override

from pysh.core.processor.processor import Processor


@dataclass(frozen=True)
class Nary[
    State,
    Result,
    ChildResult,
    ChildProcessor: Processor = Processor[State, ChildResult],
](
    Processor[State, Result],
    Sized,
    Iterable[ChildProcessor],
):
    children: Sequence[ChildProcessor] = field(default_factory=list)

    @override
    def __len__(self) -> int:
        return len(self.children)

    @override
    def __iter__(self) -> Iterator[ChildProcessor]:
        return iter(self.children)

    def _str_children(self, depth: int, sep: str) -> str:
        s = sep.join(str(child) for child in self)
        return s if depth == 0 else f"({s})"

    @classmethod
    def for_children(cls, *children: ChildProcessor) -> Self:
        return cls(children=list(children))
