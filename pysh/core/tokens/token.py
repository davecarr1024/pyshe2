from dataclasses import dataclass, field

from pysh.core.chars import Position


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    position: Position = field(default_factory=Position)
