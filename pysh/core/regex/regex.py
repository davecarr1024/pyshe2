from abc import ABC, abstractmethod
import string
from typing import Iterable, Optional, final, overload, override
from pysh.core.errors import Errorable
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


class Regex(ABC, Errorable):
    @staticmethod
    def for_str(input: str) -> "Regex":
        from pysh.core.regex.and_ import And

        return And.for_children(*[Regex.literal(c) for c in input])

    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    @override
    @final
    def __str__(self) -> str:
        return self._str(0)

    @abstractmethod
    def _str(self, depth: int) -> str: ...

    @overload
    def __call__(self, state: str) -> tuple[State, Result]: ...

    @overload
    def __call__(self, state: State) -> tuple[State, Result]: ...

    def __call__(self, state: str | State) -> tuple[State, Result]:
        match state:
            case State():
                return self._apply(state)
            case str():
                return self._apply(State.for_str(state))

    @staticmethod
    def literal(value: str) -> "Regex":
        from pysh.core.regex.literal import Literal

        return Literal(value)

    @staticmethod
    def any() -> "Regex":
        from pysh.core.regex.any import Any

        return Any()

    @staticmethod
    def class_(
        values: Iterable[str],
        display: Optional[str] = None,
    ) -> "Regex":
        from pysh.core.regex.class_ import Class

        return Class(frozenset(values), display)

    @staticmethod
    def digits() -> "Regex":
        return Regex.class_(string.digits, r"\d")

    @staticmethod
    def whitespace() -> "Regex":
        return Regex.class_(string.whitespace, r"\w")

    @staticmethod
    def range(min: str, max: str) -> "Regex":
        from pysh.core.regex.range import Range

        return Range(min, max)

    def zero_or_more(self) -> "Regex":
        from pysh.core.regex.zero_or_more import ZeroOrMore

        return ZeroOrMore(self)

    def one_or_more(self) -> "Regex":
        from pysh.core.regex.one_or_more import OneOrMore

        return OneOrMore(self)

    def zero_or_one(self) -> "Regex":
        from pysh.core.regex.zero_or_one import ZeroOrOne

        return ZeroOrOne(self)

    def __and__(self, rhs: "Regex") -> "Regex":
        from pysh.core.regex.and_ import And

        match rhs:
            case And():
                return And.for_children(self, *rhs)
            case Regex():
                return And.for_children(self, rhs)

    def __or__(self, rhs: "Regex") -> "Regex":
        from pysh.core.regex.or_ import Or

        match rhs:
            case Or():
                return Or.for_children(self, *rhs)
            case Regex():
                return Or.for_children(self, rhs)
