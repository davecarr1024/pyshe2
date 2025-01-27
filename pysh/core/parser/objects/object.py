from dataclasses import dataclass
from typing import Sequence, Type, override

from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.objects.params import Params
from pysh.core.parser.transform import Transform


@dataclass(frozen=True)
class Object[Result](
    Transform[
        Result,
        Sequence[Arg],
        Params,
    ]
):
    cls: Type[Result]

    @override
    def _transform(self, child_result: Sequence[Arg]) -> Result:
        return self.cls(**Arg.merge_as_dict(child_result))

    @override
    def _str(self, depth: int) -> str:
        return f"{self.child}.object({self.cls})"
