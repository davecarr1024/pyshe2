from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, MutableSequence, Sequence, final, override
from pysh.core.errors import Error
from pysh.core.lexer.lexer import Lexer
from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


class AbstractUntil[Result, ChildParser: Parser = Parser[Result]](
    Unary[Sequence[Result], Result, ChildParser]
):
    @abstractmethod
    def _cond(self, state: State) -> bool: ...

    @override
    @final
    def _apply(self, state: State) -> tuple[State, Sequence[Result]]:
        result: MutableSequence[Result] = []
        while not self._cond(state):
            state, child_result = self._apply_child(state)
            result.append(child_result)
        return state, result


@dataclass(frozen=True)
class Until[
    Result,
    ChildParser: Parser = Parser[Result],
    CondParser: Parser = Parser,
](
    AbstractUntil[
        Result,
        ChildParser,
    ]
):
    cond: CondParser

    @override
    def _lexer(self) -> Lexer:
        return super()._lexer() | self.cond.lexer()

    @override
    def _cond(self, state: State) -> bool:
        try:
            self.cond(state)
            return True
        except Error:
            return False

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.until({self.cond})"


class UntilEmpty[Result, ChildParser: Parser = Parser[Result]](
    AbstractUntil[Result, ChildParser]
):
    @override
    def _cond(self, state: State) -> bool:
        return state.empty()

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.until_empty()"
