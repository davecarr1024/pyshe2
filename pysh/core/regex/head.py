from abc import abstractmethod
from typing import final, override
from pysh.core.chars import Char, Stream
from pysh.core.regex.regex import Regex
from pysh.core.regex.result import Result
from pysh.core.regex.state import State


class Head(Regex):
    @abstractmethod
    def _apply_head(self, head: Char) -> Char: ...

    def _head(self, state: State) -> Char:
        return self._try(state.head)

    def _tail(self, state: State) -> State:
        return self._try(state.tail)

    @override
    @final
    def _apply(self, state: State) -> tuple[State, Result]:
        return (
            self._tail(state),
            Result.for_chars(
                self._apply_head(
                    self._head(state),
                ),
            ),
        )

    def not_(self) -> "not_.Not":
        return not_.Not(self)


from . import not_
