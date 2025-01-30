from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, final, override

from pysh.core.processor.processor import Processor
from pysh.core.processor.unary import Unary


@dataclass(frozen=True)
class AbstractTransform[
    State,
    Result,
    ChildResult,
](
    Processor[
        State,
        Result,
    ]
):
    @abstractmethod
    def _transform(self, result: ChildResult) -> Result: ...

    @abstractmethod
    def _transform_input(self, state: State) -> tuple[State, ChildResult]: ...

    @override
    @final
    def _apply(self, state: State) -> tuple[State, Result]:
        state, child_result = self._transform_input(state)
        return state, self._try(lambda: self._transform(child_result))


@dataclass(frozen=True)
class UnaryTransform[
    State,
    Result,
    ChildResult,
    ChildProcessor: Processor = Processor[State, ChildResult],
](
    Unary[
        State,
        Result,
        ChildResult,
        ChildProcessor,
    ],
    AbstractTransform[
        State,
        Result,
        ChildResult,
    ],
):
    @override
    def _transform_input(self, state: State) -> tuple[State, ChildResult]:
        return self._apply_child(state)


@dataclass(frozen=True)
class Transform[
    State,
    Result,
    ChildResult,
    ChildProcessor: Processor = Processor[State, ChildResult],
](
    UnaryTransform[
        State,
        Result,
        ChildResult,
        ChildProcessor,
    ],
):
    func: Callable[[ChildResult], Result]

    @override
    def _transform(self, result: ChildResult) -> Result:
        return self.func(result)

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.transform({self.func})"


@dataclass(frozen=True)
class TransformSelf[
    State,
    Result,
](
    AbstractTransform[
        State,
        Result,
        Result,
    ]
):
    @override
    @final
    def _transform(self, result: Result) -> Result:
        return result
