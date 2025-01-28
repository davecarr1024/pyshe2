from dataclasses import dataclass
from typing import MutableSequence, Optional, Self, Sequence, Union, cast, override

from pysh.core.lexer import Lexer, Rule
from pysh.core.parser.nary import Nary
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State


@dataclass(frozen=True)
class And[
    Result,
    ChildParser: Parser = Parser[Result],
](
    Nary[
        Sequence[Result],
        Result,
        ChildParser,
    ],
):
    @override
    def _str(self, depth: int) -> str:
        s = self._str_join(depth, " & ")
        if self._prefix is not None:
            s = f"{self._prefix} & {s}"
        if self._suffix is not None:
            s = f"{s} & {self._suffix}"
        return s

    @override
    def _apply(self, state: State) -> tuple[State, Sequence[Result]]:
        result: MutableSequence[Result] = []
        for child in self:
            state, child_result = self._apply_child(child, state)
            result.append(child_result)
        return state, result

    @override
    def __and__(  # type: ignore
        self,
        rhs: Union[
            str,
            Rule,
            ChildParser,
            Self,
        ],
    ) -> Self:
        match rhs:
            case And():
                return self.for_children(*self, *cast(Self, rhs))
            case Parser():
                return self.for_children(*self, rhs)
            case str() | Rule():
                return super().__and__(rhs)

    @override
    def __rand__(  # type:ignore
        self,
        lhs: Union[
            str,
            Rule,
            ChildParser,
        ],
    ) -> Self:
        match lhs:
            case Parser():
                return self.for_children(lhs, *self)
            case str() | Rule():
                return super().__rand__(lhs)
