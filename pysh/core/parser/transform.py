from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, final, override

from pysh.core.parser.parser import Parser
from pysh.core.parser.state import State
from pysh.core.parser.unary import Unary


@dataclass(frozen=True)
class Transform[Result, ChildResult](Unary[Result, ChildResult]):
    @abstractmethod
    def _transform(self, child_result: ChildResult) -> Result: ...

    @override
    @final
    def _apply(self, state: State) -> tuple[State, Result]:
        state, child_result = self._apply_child(state)
        return state, self._try(lambda: self._transform(child_result))

    @staticmethod
    def for_func(
        child: Parser[ChildResult],
        func: Callable[[ChildResult], Result],
    ) -> "Transform[Result,ChildResult]":
        return _FuncTransform[Result, ChildResult](child, func)


@dataclass(frozen=True)
class _FuncTransform[Result, ChildResult](Transform[Result, ChildResult]):
    func: Callable[[ChildResult], Result]

    @override
    def _transform(self, child_result: ChildResult) -> Result:
        return self._try(lambda: self.func(child_result))

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.transform({self.func})"
