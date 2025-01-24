from dataclasses import dataclass
from typing import Any, Self, Union, override

from pysh.core.parser import arg
from pysh.core.parser.and_ import And


@dataclass(frozen=True)
class Args[Object](And[arg.Setter[Object, Any]]):
    def object(self, obj: Object) -> "object.Object[Object]":
        return object.Object[Object](self, obj)

    @override
    def __and__(  # type:ignore
        self,
        rhs: Union[
            arg.Arg[Object, Any],
            "Args[Object]",
            str,
        ],
    ) -> Self:
        match rhs:
            case arg.Arg():
                return self.for_children(*self, rhs)
            case Args():
                return self.for_children(*self, *rhs)
            case str():
                return super().__and__(rhs)

    @override
    def __rand__(  # type:ignore
        self,
        lhs: Union[
            str,
            arg.Arg[
                Object,
                Any,
            ],
        ],
    ) -> Self:
        match lhs:
            case arg.Arg():
                return self.for_children(lhs, *self)
            case str():
                return super().__rand__(lhs)


from pysh.core.parser import object
