from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, override
from pysh.core.processor.processor import Processor
from pysh.core.processor.transform import AbstractTransform, UnaryTransform
from pysh.core.processor.unary import Unary


@dataclass(frozen=True)
class AbstractWhere[
    State,
    Result,
](
    AbstractTransform[
        State,
        Result,
        Result,
    ]
):
    @abstractmethod
    def _cond(self, result: Result) -> bool: ...

    @override
    def _transform(self, result: Result) -> Result:
        if not self._cond(result):
            raise self._error(f"result {result} failed cond {self}")
        return result


@dataclass(frozen=True)
class Where[
    State,
    Result,
    ChildProcessor: Processor = Processor[State, Result],
](
    UnaryTransform[
        State,
        Result,
        Result,
        ChildProcessor,
    ],
    AbstractWhere[
        State,
        Result,
    ],
):
    cond: Callable[[Result], bool]

    @override
    def _cond(self, result: Result) -> bool:
        return self.cond(result)

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.where({self.cond})"
