from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import (
    Callable,
    Generic,
    Optional,
    Self,
    Sequence,
    TypeVar,
    Union,
    final,
    overload,
    override,
)
from pysh.core import regex
from pysh.core.errors import Errorable
from pysh.core.parser.state import State

Result = TypeVar("Result", covariant=True)


@dataclass(frozen=True, kw_only=True)
class Parser(Generic[Result], ABC, Errorable):
    _prefix: Optional["Parser"] = field(default=None)
    _suffix: Optional["Parser"] = field(default=None)
    _lexer_value: Optional["lexer.Lexer"] = field(default=None)

    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    def _apply_parser[
        ChildResult
    ](self, parser: "Parser[ChildResult]", state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: parser(state))

    @final
    def lexer(self) -> "lexer.Lexer":
        lexer_ = self._lexer_value or lexer.Lexer()
        if self._prefix is not None:
            lexer_ |= self._prefix.lexer()
        if self._suffix is not None:
            lexer_ |= self._suffix.lexer()
        return lexer_ | self._lexer()

    @abstractmethod
    def _lexer(self) -> "lexer.Lexer": ...

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

    def with_lexer(
        self,
        lexer_: Union[
            "lexer.Lexer",
            "lexer_rule.Rule",
        ],
    ) -> Self:
        return replace(self, _lexer_value=(self._lexer_value or lexer.Lexer()) | lexer_)

    def ignore_whitespace(self) -> Self:
        return self.with_lexer(
            lexer.Lexer.for_rules(
                lexer_rule.Rule.for_str(
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

    def until(self, cond: "Parser") -> "Parser[Sequence[Result]]":
        from .until import Until

        return Until[Result](self, cond)

    def until_empty(self) -> "Parser[Sequence[Result]]":
        from .until import UntilEmpty

        return UntilEmpty[Result](self)

    def zero_or_more(self) -> "Parser[Sequence[Result]]":
        from .zero_or_more import ZeroOrMore

        return ZeroOrMore[Result](self)

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


from pysh.core.lexer import lexer, rule as lexer_rule
from . import and_, or_, head
from .objects import param
