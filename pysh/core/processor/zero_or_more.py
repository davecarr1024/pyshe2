from dataclasses import dataclass
from typing import MutableSequence, Sequence, override
from pysh.core.processor.combiner import AbstractCombiner, CombineSelf
from pysh.core.processor.processor import Processor
from pysh.core.processor.transform import AbstractTransform, UnaryTransform
from pysh.core.processor.unary import Unary


@dataclass(frozen=True)
class AbstractZeroOrMore[
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
    AbstractCombiner[
        State,
        Result,
        ChildResult,
    ],
):
    @override
    def _transform_input(self, state: State) -> tuple[State, Sequence[ChildResult]]:
        result: MutableSequence[ChildResult] = []
        while True:
            try:
                state, child_result = self._apply_child(state)
                result.append(child_result)
            except Processor.Error:
                return state, result

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}*"


@dataclass(frozen=True)
class ZeroOrMore[
    State,
    Result,
    ChildProcessor: Processor = Processor[State, Result],
](
    CombineSelf[
        State,
        Result,
    ],
    AbstractZeroOrMore[
        State,
        Sequence[Result],
        Result,
        ChildProcessor,
    ],
): ...
