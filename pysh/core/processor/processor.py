from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Any, Callable, Optional, Self, Sequence, final, override
from pysh.core.errors import Errorable


@dataclass(frozen=True)
class Processor[State, Result](ABC, Errorable):
    _prefix: Optional["Processor[State, Any]"] = field(kw_only=True, default=None)
    _suffix: Optional["Processor[State,Any]"] = field(kw_only=True, default=None)

    @abstractmethod
    def _apply(self, state: State) -> tuple[State, Result]: ...

    def _apply_processor[
        ChildResult
    ](self, processor: "Processor[State,ChildResult]", state: State) -> tuple[
        State, ChildResult
    ]:
        return self._try(lambda: processor(state))

    @final
    def __call__(self, state: State) -> tuple[State, Result]:
        if self._prefix is not None:
            state, _ = self._prefix(state)
        state, result = self._apply(state)
        if self._suffix is not None:
            state, _ = self._suffix(state)
        return state, result

    @override
    @final
    def __str__(self) -> str:
        s = self._str(0)
        if self._prefix is not None:
            s += f".prefix({self._prefix})"
        if self._suffix is not None:
            s += f".suffix({self._suffix})"
        return s

    @abstractmethod
    def _str(self, depth: int) -> str: ...

    def prefix(self, prefix: "Processor[State,Any]") -> Self:
        if self._prefix is not None:
            raise self._error(f"trying to overwrite prefix {prefix}")
        return replace(self, _prefix=prefix)

    def suffix(self, suffix: "Processor[State,Any]") -> Self:
        if self._suffix is not None:
            raise self._error(f"trying to overwrite suffix {suffix}")
        return replace(self, _suffix=suffix)

    def transform[T](self, func: Callable[[Result], T]) -> "Processor[State,T]":
        from .transform import Transform

        return Transform[State, T, Result](self, func)

    def where(self, cond: Callable[[Result], bool]) -> "Processor[State,Result]":
        from .where import Where

        return Where[State, Result](self, cond)

    def until(
        self, cond: "Processor[State,Any]"
    ) -> "Processor[State,Sequence[Result]]":
        from .until import Until

        return Until[State, Result](self, cond)

    def zero_or_more(self) -> "Processor[State,Sequence[Result]]":
        from .zero_or_more import ZeroOrMore

        return ZeroOrMore[State, Result](self)

    def __and__(
        self, rhs: "Processor[State,Result]"
    ) -> "Processor[State,Sequence[Result]]":
        from .and_ import And

        match rhs:
            case And():
                return And[State, Result].for_children(self, *rhs)
            case Processor():
                return And[State, Result].for_children(self, rhs)

