from typing import Sequence
from pysh.core.parser.parser import Parser

type Composite[Result] = Parser[Sequence[Result]]
