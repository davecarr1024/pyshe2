from dataclasses import dataclass
from typing import Self, Union, overload, override
from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.parser import Parser
from pysh.core.parser.transform import Transform


@dataclass(frozen=True)
class Param[Result](Transform[Arg[Result], Result, Parser[Result]]):
    name: str

    @override
    def _transform(self, child_result: Result) -> Arg[Result]:
        return Arg[Result](self.name, child_result)

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.param({self.name})"

    @overload
    def __and__(self, rhs: str) -> Self: ...

    @overload
    def __and__(self, rhs: "Param") -> "params.Params": ...

    @override
    def __and__(  # type:ignore
        self,
        rhs: Union[
            str,
            "Param",
            "params.Params",
        ],
    ) -> Union[
        Self,
        "params.Params",
    ]:
        match rhs:
            case Param():
                return params.Params.for_children(self, rhs)
            case params.Params():
                return params.Params.for_children(self, *rhs)
            case str():
                return super().__and__(rhs)


from . import params
