from dataclasses import dataclass

from pysh.core.processor.processor import Processor


@dataclass(frozen=True)
class Unary[
    State,
    Result,
    ChildResult,
    ChildProcessor: Processor = Processor[State, ChildResult],
](Processor[State, Result]):
    child: ChildProcessor

    def _apply_child(self, state: State) -> tuple[State, ChildResult]:
        return self._try(lambda: self._apply_processor(self.child, state))
