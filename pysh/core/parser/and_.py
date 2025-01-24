from dataclasses import dataclass
from types import NotImplementedType
from typing import MutableSequence, Optional, Self, Sequence, Union, overload, override

from pysh.core.parser.nary import Nary
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.suffix import Suffix
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class And[Result](Nary[Sequence[Result], Result]):
    _prefix: Optional[Parser] = None
    _suffix: Optional[Parser] = None

    @override
    def _str(self, depth: int) -> str:
        return self._str_join(depth, " & ")

    @override
    def _apply(self, state: State) -> tuple[State, Sequence[Result]]:
        result: MutableSequence[Result] = []
        if self._prefix is not None:
            state, _ = self._apply_parser(self._prefix, state)
        for child in self:
            state, child_result = self._apply_child(child, state)
            result.append(child_result)
        if self._suffix is not None:
            state, _ = self._apply_parser(self._suffix, state)
        return state, result

    def _with(
        self,
        *,
        prefix: Optional[Parser] = None,
        suffix: Optional[Parser] = None,
    ) -> Self:
        return self.__class__(
            children=self.children,
            _prefix=prefix,
            _suffix=suffix,
        )

    @override
    def __and__(  # type: ignore
        self,
        rhs: Union[
            str,
            Parser[Result],
            "And[Result]",
        ],
    ) -> Self:
        match rhs:
            case And():
                return self.for_children(*self, *rhs)
            case Parser():
                return self.for_children(*self, rhs)
            case str():
                return self._with(prefix=self.head(rhs))

    @override
    def __rand__(  # type:ignore
        self,
        lhs: Union[
            str,
            Parser[Result],
        ],
    ) -> Self:
        match lhs:
            case str():
                return self._with(suffix=self.head(lhs))
            case Parser():
                return self.for_children(lhs, *self)
