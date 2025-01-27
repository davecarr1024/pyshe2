from dataclasses import dataclass
from typing import Self, override

from pysh.core.parser.and_ import And
from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.objects.param import Param


@dataclass(frozen=True)
class Params(And[Arg, Param]):
    @override
    def __and__(self, rhs: str | Param | Self) -> Self:
        match rhs:
            case str():
                return super().__and__(rhs)
            case Param():
                return self.for_children(*self, rhs)
            case Params():
                return self.for_children(*self, *rhs)

    @override
    def __rand__(self, lhs: str | Param) -> Self:
        match lhs:
            case str():
                return super().__rand__(lhs)
            case Param():
                return self.for_children(lhs, *self)
