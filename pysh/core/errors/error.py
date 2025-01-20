from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence, Sized, final, override


@dataclass(kw_only=True)
class Error(
    Exception,
    Sized,
    Iterable["Error"],
):
    msg: Optional[str] = None
    children: Sequence["Error"] = field(default_factory=list)

    @override
    @final
    def __str__(self) -> str:
        return self._str(0)

    def _str_line(self) -> str:
        return self.msg or "<no message>"

    def _str(self, tabs: int = 0) -> str:
        return "\n".join(
            [f'{"  "*tabs}{self._str_line()}']
            + [child._str(tabs + 1) for child in self]
        )

    @override
    def __iter__(self) -> Iterator["Error"]:
        return iter(self.children)

    @override
    def __len__(self) -> int:
        return len(self.children)
