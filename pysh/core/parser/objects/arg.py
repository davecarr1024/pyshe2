from dataclasses import dataclass
from typing import override


@dataclass(frozen=True)
class Arg[T]:
    name: str
    value: T

    @override
    def __str__(self) -> str:
        return f"{self.name} = {self.value}"
