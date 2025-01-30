from dataclasses import dataclass
from typing import Sequence, override
from pysh.core.processor.transform import AbstractTransform, TransformSelf


@dataclass(frozen=True)
class AbstractCombiner[
    State,
    Result,
    ChildResult,
](
    AbstractTransform[
        State,
        Result,
        Sequence[ChildResult],
    ]
): ...


@dataclass(frozen=True)
class CombineSelf[
    State,
    Result,
](
    TransformSelf[
        State,
        Sequence[Result],
    ],
    AbstractCombiner[
        State,
        Sequence[Result],
        Result,
    ],
): ...
