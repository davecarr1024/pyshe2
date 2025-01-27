from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence, Sized, override

from pysh.core.parser.objects.arg import Arg


@dataclass(frozen=True)
class Args(Sized, Iterable[Arg]):
    args: Sequence[Arg] = field(default_factory=list)

    @override
    def __str__(self) -> str:
        return f"({', '.join(str(arg) for arg in self)})"

    @override
    def __len__(self) -> int:
        return len(self.args)

    @override
    def __iter__(self) -> Iterator[Arg]:
        return iter(self.args)
