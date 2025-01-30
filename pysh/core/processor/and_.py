from dataclasses import dataclass
from typing import MutableSequence, Sequence, override
from pysh.core.processor.combiner import AbstractCombiner, CombineSelf
from pysh.core.processor.nary import Nary
from pysh.core.processor.processor import Processor


@dataclass(frozen=True)
class AbstractAnd[
    State,
    Result,
    ChildResult,
    ChildProcessor: Processor = Processor[State, ChildResult],
](
    Nary[
        State,
        Result,
        ChildResult,
        ChildProcessor,
    ],
    AbstractCombiner[
        State,
        Result,
        ChildResult,
    ],
):
    @override
    def _str(self, depth: int) -> str:
        return self._str_children(depth, " & ")

    @override
    def _transform_input(self, state: State) -> tuple[State, Sequence[ChildResult]]:
        result: MutableSequence[ChildResult] = []
        for child in self:
            state, child_result = self._apply_processor(child, state)
            result.append(child_result)
        return state, result


@dataclass(frozen=True)
class And[
    State,
    Result,
    ChildProcessor: Processor = Processor[State, Result],
](
    CombineSelf[
        State,
        Result,
    ],
    AbstractAnd[
        State,
        Sequence[Result],
        Result,
        ChildProcessor,
    ],
): ...
