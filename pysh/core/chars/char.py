from dataclasses import dataclass, field
from typing import override

from pysh.core.chars import Position
from pysh.core.errors import Errorable


@dataclass(frozen=True)
class Char(Errorable):
    value: str
    position: Position = field(default_factory=Position)

    def __post_init__(self) -> None:
        if len(self.value) != 1:
            raise self._error(f"invalid value {self.value}")

    @override
    def __str__(self) -> str:
        return f"{self.value}@{self.position}"
