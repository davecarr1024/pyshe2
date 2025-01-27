from dataclasses import dataclass
from typing import MutableSequence, Optional, Self, Sequence, Union, cast, override

from pysh.core.lexer import Lexer
from pysh.core.parser.affixes.affixable import Affixable
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
    Affixable[Sequence[Result]],
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
    def lexer(self) -> Lexer:
        return super().lexer() | super(Affixable, self).lexer()

    @override
    def _apply_in_affixes(self, state: State) -> tuple[State, Sequence[Result]]:
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
            ChildParser,
            Self,
        ],
    ) -> Self:
        match rhs:
            case And():
                return self.for_children(*self, *cast(Self, rhs))
            case Parser():
                return self.for_children(*self, rhs)
            case str():
                return self._with_suffix(self.head(rhs))

    @override
    def __rand__(  # type:ignore
        self,
        lhs: Union[
            str,
            ChildParser,
        ],
    ) -> Self:
        match lhs:
            case str():
                return self._with_prefix(self.head(lhs))
            case Parser():
                return self.for_children(lhs, *self)
