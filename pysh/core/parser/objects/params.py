from dataclasses import dataclass

from pysh.core.parser.and_ import And
from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.objects.param import Param


@dataclass(frozen=True)
class Params(And[Arg, Param]): ...
