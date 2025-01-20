from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    line: int = 0
    column: int = 0
