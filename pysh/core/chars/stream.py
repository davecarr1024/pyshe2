from dataclasses import dataclass
from typing import MutableSequence, Optional

from pysh.core import streams
from pysh.core.chars import Char, Position


@dataclass(frozen=True)
class Stream(streams.Stream[Char]):
    @classmethod
    def for_str(cls, value: str, position: Optional[Position] = None) -> "Stream":
        position = position or Position()
        chars: MutableSequence[Char] = []
        for c in value:
            chars.append(Char(c, position))
            if c == "\n":
                position = Position(position.line + 1, 0)
            else:
                position = Position(position.line, position.column + 1)
        return cls(chars)
