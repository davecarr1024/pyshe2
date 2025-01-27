from dataclasses import dataclass
from typing import Optional, Self

from pysh.core.parser import Parser, State
from pysh.core.regex import Regex, one_or_more


@dataclass(frozen=True)
class Int:
    value: int

    @classmethod
    def parser(cls) -> Parser[Self]:
        return (
            Parser.head("int", Regex.digits().one_or_more())
            .value()
            .transform(int)
            .transform(cls)
        )


@dataclass(frozen=True)
class Decl:
    name: str = ""
    value: Optional[Int] = None

    @classmethod
    def parser(cls) -> Parser[Self]:
        return (
            (
                Parser.head(
                    "id", (Regex.range("a", "z") | Regex.range("A", "Z")).one_or_more()
                )
                .value()
                .arg("name")
                & "="
                & Int.parser().arg("value")
            )
            .object(cls())
            .ignore_whitespace()
        )


def test_parse():
    assert Decl.parser()("value = 123") == (State(), Decl("value", Int(123)))
