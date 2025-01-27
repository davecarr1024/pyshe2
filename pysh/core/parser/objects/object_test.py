from dataclasses import dataclass
from typing import Self

from pysh.core.parser import Parser, State
from pysh.core.regex import Regex, one_or_more


@dataclass(frozen=True)
class _Obj:
    i: int
    s: str

    @classmethod
    def parser(cls) -> Parser["_Obj"]:
        return (
            (
                Parser.head("int", Regex.digits().one_or_more())
                .value()
                .transform(int)
                .param("i")
                & Parser.head("str", Regex.range("a", "z").one_or_more())
                .value()
                .param("s")
            )
            .ignore_whitespace()
            .object(_Obj)
        )


def test_apply():
    assert _Obj.parser()("123 abc") == (State(), _Obj(123, "abc"))
