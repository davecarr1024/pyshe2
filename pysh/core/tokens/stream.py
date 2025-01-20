from dataclasses import dataclass

from pysh.core import streams
from pysh.core.tokens.token import Token


@dataclass(frozen=True)
class Stream(streams.Stream[Token]): ...
