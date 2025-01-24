from abc import ABC, abstractmethod
from typing import Callable, Union, final, override

from pysh.core import regex
from pysh.core.errors import Errorable
from pysh.core.lexer import Lexer
from pysh.core.parser.state import State
from pysh.core.tokens import Token


class Parser[Result](ABC, Errorable):
    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    def _apply_parser[
        ChildResult
    ](self, parser: "Parser[ChildResult]", state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: parser._apply(state))

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
    def head(name: str, value: None | str | regex.Regex = None) -> "head.Head":
        return head.Head.for_str(name, value)

    def with_lexer(self, lexer: Lexer) -> "Parser[Result]":
        from pysh.core.parser.with_lexer import WithLexer

        return WithLexer[Result](self, lexer)

    def prefix(self, prefix: Union["Parser", str]) -> "Parser[Result]":
        from pysh.core.parser.prefix import Prefix

        match prefix:
            case Parser():
                return Prefix(self, prefix)
            case str():
                return Prefix(self, self.head(prefix))

    def suffix(self, suffix: Union["Parser", str]) -> "Parser[Result]":
        from pysh.core.parser.suffix import Suffix

        match suffix:
            case Parser():
                return Suffix(self, suffix)
            case str():
                return Suffix(self, self.head(suffix))

    def transform[T](self, func: Callable[[Result], T]) -> "Parser[T]":
        from pysh.core.parser.transform import Transform

        return Transform[T, Result].for_func(self, func)

    def arg[
        Object
    ](
        self,
        value: Union[
            Callable[[Object, Result], Object],
            str,
        ],
    ) -> "arg.Arg[Object,Result]":
        match value:
            case str():
                return arg.Arg[Object, Result].for_dataclass_property(self, value)
            case _:
                return arg.Arg[Object, Result](self, value)

    def __and__(
        self,
        rhs: Union[
            str,
            "Parser[Result]",
        ],
    ) -> "and_.And[Result]":
        match rhs:
            case and_.And():
                return and_.And[Result].for_children(self, *rhs)
            case Parser():
                return and_.And[Result].for_children(self, rhs)
            case str():
                return and_.And[Result].for_children(self.suffix(rhs))

    def __rand__(
        self,
        lhs: Union[
            str,
            "Parser[Result]",
        ],
    ) -> "and_.And[Result]":
        match lhs:
            case Parser():
                return and_.And[Result].for_children(lhs, self)
            case str():
                return and_.And[Result].for_children(self.prefix(lhs))

    def __or__(self, rhs: "Parser[Result]") -> "or_.Or[Result]":
        match rhs:
            case or_.Or():
                return or_.Or[Result].for_children(self, *rhs)
            case Parser():
                return or_.Or[Result].for_children(self, rhs)


from . import and_, or_, head, arg
