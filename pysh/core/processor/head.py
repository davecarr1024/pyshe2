from dataclasses import dataclass
from typing import override

from pysh.core.processor.processor import Processor
from pysh.core.streams import AbstractStream


@dataclass(frozen=True)
class Head[
    State: AbstractStream,
    Result,
](
    Processor[
        State,
        Result,
    ],
):
    def _head(self, state: State) -> Result:
        return self._try(state.head)

    def _tail(self, state: State) -> State:
        return self._try(state.tail)

    @override
    def _apply(self, state: State) -> tuple[State, Result]:
        return self._tail(state), self._head(state)

    @override
    def _str(self, depth: int) -> str:
        return "head()"


@dataclass(frozen=True)
class Headable[
    State: AbstractStream,
    Result,
](
    Processor[
        State,
        Result,
    ]
):
    @classmethod
    def head(cls) -> Head[State, Result]:
        return Head[State, Result]()
