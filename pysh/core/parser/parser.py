from abc import ABC, abstractmethod
from typing import Self, Sequence, Union, final, overload, override

from pysh.core import regex
from pysh.core.errors import Errorable
from pysh.core.lexer import Lexer
from pysh.core.parser import composite
from pysh.core.parser.state import State
from pysh.core.tokens import Token


class Parser[Result](ABC, Errorable):
    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    @abstractmethod
    def lexer(self) -> Lexer: ...

    @final
    def __call__(self, state: str | regex.State | State) -> tuple[State, Result]:
        match state:
            case str() | regex.State():

                def fix_state(state: str | regex.State) -> State:
                    return State.for_tokens(*self._try(lambda: self.lexer()(state)))

                state = fix_state(state)
        return self._apply(state)

    @override
    @final
    def __str__(self) -> str:
        return self._str(0)

    @abstractmethod
    def _str(self, depth: int) -> str: ...

    @staticmethod
    def head(name: str, value: None | str | regex.Regex = None) -> "Parser[Token]":
        from pysh.core.parser.head import Head

        return Head.for_str(name, value)

    def with_lexer(self, lexer: Lexer) -> "Parser[Result]":
        from pysh.core.parser.with_lexer import WithLexer

        return WithLexer[Result](self, lexer)

    def suffix(self, suffix: "Parser") -> "Parser[Result]":
        from pysh.core.parser.suffix import Suffix

        return Suffix(self, suffix)

    def __and__(
        self,
        rhs: Union[
            str,
            "Parser[Result]",
        ],
    ) -> "Parser[Sequence[Result]]":
        from pysh.core.parser.and_ import And

        match rhs:
            case And():
                return And[Result].for_children(self, *rhs)
            case Parser():
                return And[Result].for_children(self, rhs)
            case str():
                return And[Result].for_children(self.suffix(self.head(rhs)))
