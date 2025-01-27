from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Callable, Optional, Self, Union, final, overload, override

from pysh.core import regex
from pysh.core.errors import Errorable
from pysh.core.lexer import Lexer, Rule
from pysh.core.parser.state import State
from pysh.core.tokens import Token


@dataclass(frozen=True, kw_only=True)
class Parser[Result](ABC, Errorable):
    _prefix: Optional["Parser"] = field(default=None)
    _suffix: Optional["Parser"] = field(default=None)
    _lexer_value: Optional[Lexer] = field(default=None)

    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    def _apply_parser[
        ChildResult
    ](self, parser: "Parser[ChildResult]", state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: parser(state))

    @final
    def lexer(self) -> Lexer:
        lexer = self._lexer_value or Lexer()
        if self._prefix is not None:
            lexer |= self._prefix.lexer()
        if self._suffix is not None:
            lexer |= self._suffix.lexer()
        return lexer | self._lexer()

    @abstractmethod
    def _lexer(self) -> Lexer: ...

    @final
    def __call__(self, state: str | regex.State | State) -> tuple[State, Result]:
        match state:
            case str() | regex.State():

                def fix_state(state: str | regex.State) -> State:
                    return State.for_tokens(*self._try(lambda: self.lexer()(state)))

                state = fix_state(state)
        return self.__call(state)

    @final
    def __call(self, state: State) -> tuple[State, Result]:
        if self._prefix is not None:
            state, _ = self._apply_parser(self._prefix, state)
        state, result = self._apply(state)
        if self._suffix is not None:
            state, _ = self._apply_parser(self._suffix, state)
        return state, result

    def prefix(self, prefix: Union["Parser", str]) -> Self:
        if self._prefix is not None:
            raise self._error(f"trying to set multiple prefixes {prefix}")
        if isinstance(prefix, str):
            prefix = self.head(prefix)
        return replace(self, _prefix=prefix)

    def suffix(self, suffix: Union["Parser", str]) -> Self:
        if self._suffix is not None:
            raise self._error(f"trying to set multiple suffixes {suffix}")
        if isinstance(suffix, str):
            suffix = self.head(suffix)
        return replace(self, _suffix=suffix)

    @override
    @final
    def __str__(self) -> str:
        s = self._str(0)
        if self._prefix is not None:
            s = f"{self._prefix} & {s}"
        if self._suffix is not None:
            s = f"{s} & {self._suffix}"
        return s

    @abstractmethod
    def _str(self, depth: int) -> str: ...

    @staticmethod
    def head(name: str, value: None | str | regex.Regex = None) -> "head.Head":
        return head.Head.for_str(name, value)

    def with_lexer(self, lexer: Lexer) -> Self:
        return replace(self, _lexer_value=(self._lexer_value or Lexer()) | lexer)

    def ignore_whitespace(self) -> Self:
        return self.with_lexer(
            Lexer.for_rules(
                Rule.for_str(
                    "ws",
                    regex.Regex.whitespace().one_or_more(),
                    False,
                )
            )
        )

    def transform[T](self, func: Callable[[Result], T]) -> "Parser[T]":
        from pysh.core.parser.transform import Transform

        return Transform[T, Result, Parser[Result]].for_func(self, func)

    def param(self, name: str) -> "param.Param[Result]":
        return param.Param[Result](self, name)

    @overload
    def __and__(self, rhs: str) -> Self: ...

    @overload
    def __and__(self, rhs: "Parser[Result]") -> "and_.And[Result]": ...

    def __and__(
        self,
        rhs: Union[
            str,
            "Parser[Result]",
        ],
    ) -> Union["and_.And[Result]", Self]:
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
    ) -> Self:
        return self.prefix(lhs)

    def __or__(self, rhs: "Parser[Result]") -> "or_.Or[Result]":
        match rhs:
            case or_.Or():
                return or_.Or[Result].for_children(self, *rhs)
            case Parser():
                return or_.Or[Result].for_children(self, rhs)


from . import and_, or_, head
from .objects import param
