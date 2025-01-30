from dataclasses import dataclass
from pysh.core.processor import Headable
from pysh.core.regex.state import State
from pysh.core.regex.result import Result


@dataclass(frozen=True)
class Regex(Headable[State, Result]): ...
