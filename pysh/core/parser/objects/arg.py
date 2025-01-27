from dataclasses import dataclass
from typing import Any, Sequence, override


@dataclass(frozen=True)
class Arg[T]:
    name: str
    value: T

    @override
    def __str__(self) -> str:
        return f"{self.name} = {self.value}"

    def as_dict(self) -> dict[str, Any]:
        return {self.name: self.value}

    @staticmethod
    def merge_as_dict(args: Sequence["Arg"]) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for arg in args:
            values |= arg.as_dict()
        return values
