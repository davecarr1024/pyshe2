from abc import ABC, abstractmethod
from typing import Callable, Union, final, overload, override

from pysh.core import regex
from pysh.core.errors import Errorable
from pysh.core.lexer import Lexer, Rule
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

    def ignore_whitespace(self) -> "Parser[Result]":
        return self.with_lexer(
            Lexer.for_rules(
                Rule.for_str(
                    "ws",
                    regex.Regex.whitespace().one_or_more(),
                    False,
                )
            )
        )

    def prefix(self, value: Union["Parser", str]) -> "prefix_lib.Prefix[Result]":
        match value:
            case Parser():
                return prefix_lib.Prefix(self, value)
            case str():
                return prefix_lib.Prefix(self, self.head(value))

    def suffix(self, value: Union["Parser", str]) -> "suffix_lib.Suffix[Result]":
        match value:
            case Parser():
                return suffix_lib.Suffix(self, value)
            case str():
                return suffix_lib.Suffix(self, self.head(value))

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

    @overload
    def __and__(self, rhs: str) -> "suffix_lib.Suffix[Result]": ...

    @overload
    def __and__(self, rhs: "Parser[Result]") -> "and_.And[Result]": ...

    def __and__(
        self,
        rhs: Union[
            str,
            "Parser[Result]",
        ],
    ) -> Union["and_.And[Result]", "suffix_lib.Suffix[Result]"]:
        match rhs:
            case and_.And():
                return and_.And[Result].for_children(self, *rhs)
            case Parser():
                return and_.And[Result].for_children(self, rhs)
            case str():
                return self.suffix(rhs)

    def __rand__(
        self,
        lhs: str,
    ) -> "prefix_lib.Prefix[Result]":
        return self.prefix(lhs)

    def __or__(self, rhs: "Parser[Result]") -> "or_.Or[Result]":
        match rhs:
            case or_.Or():
                return or_.Or[Result].for_children(self, *rhs)
            case Parser():
                return or_.Or[Result].for_children(self, rhs)


from . import and_, or_, head, arg, prefix as prefix_lib, suffix as suffix_lib
