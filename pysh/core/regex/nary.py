from dataclasses import dataclass, field
from typing import Iterable, Iterator, Self, Sequence, Sized, override

from pysh.core.regex.regex import Regex
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


@dataclass(frozen=True)
class Nary(Regex, Sized, Iterable[Regex]):
    children: Sequence[Regex] = field(default_factory=tuple)

    @override
    def __len__(self) -> int:
        return len(self.children)

    @override
    def __iter__(self) -> Iterator[Regex]:
        return iter(self.children)

    def _apply_child(self, child: Regex, state: State) -> tuple[State, Result]:
        if child not in self:
            raise self._error(f"unknown child {child} in {self}")
        return self._try(lambda: child._apply(state))

    @classmethod
    def for_children(cls, *children: Regex) -> Regex:
        if len(children) == 1:
            return children[0]
        else:
            return cls(tuple(children))
