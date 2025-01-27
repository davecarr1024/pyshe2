from dataclasses import dataclass
from typing import Type

from pysh.core.parser.and_ import And
from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.objects.param import Param
from pysh.core.parser.parser import Parser


@dataclass(frozen=True)
class Params(And[Arg, Param]):
    def object[Result](self, cls: Type[Result]) -> Parser[Result]:
        from .object import Object

        return Object[Result](self, cls)
