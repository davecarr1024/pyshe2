from dataclasses import dataclass
from typing import Self, Union, overload, override

from pysh.core.parser.affixes.affixable import Affixable
from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Param[T](Unary[Arg[T], T], Affixable[Arg[T]]):
    name: str

    @override
    def _apply_in_affixes(self, state: State) -> tuple[State, Arg[T]]:
        state, value = self._apply_child(state)
        return state, Arg[T](self.name, value)

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.param({self.param})"

    @overload
    def __and__(self, rhs: str) -> Self: ...

    @overload
    def __and__(self, rhs: Self) -> "params.Params": ...

    @override
    def __and__(  # type:ignore
        self,
        rhs: Union[
            str,
            Self,
        ],
    ) -> Union[
        Self,
        "params.Params",
    ]:
        match rhs:
            case Param():
                return params.Params.for_children(self, rhs)
            case str():
                return self._with_suffix(self.head(rhs))

    @override
    def __rand__(self, lhs: str) -> Self:
        return self._with_prefix(self.head(lhs))


from . import params
