from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, MutableSequence, Sequence, final, override

from pysh.core.processor.processor import Processor
from pysh.core.processor.unary import Unary


@dataclass(frozen=True)
class AbstractUntil[
    State,
    Result,
    ChildProcessor: Processor = Processor[State, Result],
](
    Unary[
        State,
        Sequence[Result],
        Result,
        ChildProcessor,
    ]
):
    @abstractmethod
    def _cond(self, state: State) -> bool: ...

    @override
    @final
    def _apply(self, state: State) -> tuple[State, Sequence[Result]]:
        result: MutableSequence[Result] = []
        while True:
            if self._cond(state):
                return state, result
            state, child_result = self._apply_child(state)
            result.append(child_result)


@dataclass(frozen=True)
class Until[
    State,
    Result,
    ChildProcessor: Processor = Processor[State, Result],
    CondProcessor: Processor = Processor[State, Any],
](
    AbstractUntil[
        State,
        Result,
        ChildProcessor,
    ]
):
    cond: CondProcessor

    @override
    def _cond(self, state: State) -> bool:
        try:
            self.cond(state)
            return True
        except Processor.Error:
            return False

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.until({self.cond})"
