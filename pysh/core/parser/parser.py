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
from pysh.core.errors import Errorable
from pysh.core.lexer import Lexer, Rule as LexRule
from pysh.core.parser.state import State
from pysh.core.regex import Regex, State as RegexState

Result = TypeVar("Result", covariant=True)


@dataclass(frozen=True, kw_only=True)
class Parser(Generic[Result], ABC, Errorable):
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
    def __call__(self, state: str | RegexState | State) -> tuple[State, Result]:
        match state:
            case str() | RegexState():

                def fix_state(state: str | RegexState) -> State:
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

    @classmethod
    def _affix_value(
        cls,
        value: Union[
            "Parser",
            str,
            LexRule,
        ],
    ) -> "Parser":
        match value:
            case Parser():
                return value
            case str():
                return cls.head(value)
            case LexRule():
                return head.Head(value)

    def prefix(
        self,
        value: Union[
            "Parser",
            str,
            LexRule,
        ],
    ) -> Self:
        if self._prefix is not None:
            raise self._error(f"trying to overwrite prefix with {value}")
        return replace(self, _prefix=self._affix_value(value))

    def suffix(
        self,
        value: Union[
            "Parser",
            str,
            LexRule,
        ],
    ) -> Self:
        if self._suffix is not None:
            raise self._error(f"trying to set multiple suffixes {value}")
        return replace(self, _suffix=self._affix_value(value))

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

    @overload
    @staticmethod
    def head(name: str) -> "head.Head": ...

    @overload
    @staticmethod
    def head(name: str, value: str) -> "head.Head": ...

    @overload
    @staticmethod
    def head(name: str, value: Regex) -> "head.Head": ...

    @overload
    @staticmethod
    def head(name: LexRule) -> "head.Head": ...

    @staticmethod
    def head(name: str | LexRule, value: None | str | Regex = None) -> "head.Head":
        match name:
            case str():
                return head.Head.for_str(name, value)
            case LexRule():
                return head.Head(name)

    def with_lexer(
        self,
        lexer: Union[
            Lexer,
            LexRule,
        ],
    ) -> Self:
        return replace(self, _lexer_value=(self._lexer_value or Lexer()) | lexer)

    def ignore_whitespace(self) -> Self:
        return self.with_lexer(
            LexRule.for_str(
                "ws",
                Regex.whitespace().one_or_more(),
                False,
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

    def one_or_more(self) -> "Parser[Sequence[Result]]":
        from .one_or_more import OneOrMore

        return OneOrMore[Result](self)

    def zero_or_one(self) -> "Parser[Optional[Result]]":
        from .zero_or_one import ZeroOrOne

        return ZeroOrOne[Result](self)

    @overload
    def __and__(self, rhs: str | LexRule) -> Self: ...

    @overload
    def __and__(self, rhs: "Parser[Result]") -> "and_.And[Result]": ...

    def __and__(
        self,
        rhs: Union[
            str,
            LexRule,
            "Parser[Result]",
        ],
    ) -> Union["and_.And[Result]", Self]:
        match rhs:
            case and_.And():
                return and_.And[Result].for_children(self, *rhs)
            case Parser():
                return and_.And[Result].for_children(self, rhs)
            case str() | LexRule():
                return self.suffix(rhs)

    def __rand__(
        self,
        lhs: str | LexRule,
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
