from dataclasses import dataclass
import dataclasses
from typing import Any, Callable, Self, Union, override

from pysh.core.errors import Error, Errorable
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Setter[Object, Result](Errorable):
    func: Callable[[Object, Result], Object]
    value: Result

    def __call__(self, obj: Object) -> Object:
        return self._try(lambda: self.func(obj, self.value))

    @staticmethod
    def dataclass_property_setter(name: str) -> Callable[[Object, Result], Object]:
        def set(object: Object, value: Result) -> Object:
            if not dataclasses.is_dataclass(object):
                raise Error(
                    msg=f"using dataclass arg setter for non-dataclass {object}"
                )
            return dataclasses.replace(object, **{name: value})  # type:ignore

        return set


@dataclass(frozen=True)
class Arg[Object, Result](Unary[Setter[Object, Result], Result]):
    func: Callable[[Object, Result], Object]

    @classmethod
    def for_dataclass_property(
        cls,
        child: Parser[Result],
        name: str,
    ) -> Self:
        return cls(
            child,
            Setter[Object, Result].dataclass_property_setter(name),
        )

    @override
    def _apply(self, state: State) -> tuple[State, Setter[Object, Result]]:
        state, result = self._apply_child(state)
        return state, Setter[Object, Result](self.func, result)

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.arg()"

    @override
    def __and__(  # type:ignore
        self,
        rhs: Union[
            "Arg[Object,Any]",
            "args.Args[Object]",
            str,
        ],
    ) -> "args.Args[Object]":
        match rhs:
            case Arg():
                return args.Args[Object].for_children(self, rhs)
            case args.Args():
                return args.Args[Object].for_children(self, *rhs)
            case str():
                return args.Args[Object].for_children(self.suffix(rhs))

    @override
    def __rand__(  # type:ignore
        self,
        lhs: Union[str, "Arg[Object,Any]"],
    ) -> "args.Args[Object]":
        match lhs:
            case str():
                return args.Args[Object].for_children(self.prefix(lhs))
            case Arg():
                return args.Args[Object].for_children(lhs, self)


from . import args
