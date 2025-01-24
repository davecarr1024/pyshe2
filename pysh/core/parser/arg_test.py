from dataclasses import dataclass

from pysh.core.parser import Parser, State
from pysh.core.regex import Regex


@dataclass(frozen=True)
class Int:
    value: int


def test_set_by_name():
    state, setter = (
        Parser.head("int", Regex.digits().one_or_more())
        .value()
        .transform(int)
        .arg("value")("123")
    )
    assert state == State()
    assert setter(Int(0)) == Int(123)


def test_set_by_func():
    state, setter = (
        Parser.head("int", Regex.digits().one_or_more())
        .value()
        .transform(int)
        .arg(lambda _, v: Int(v))("123")
    )
    assert state == State()
    assert setter(Int(0)) == Int(123)


def test_prefix():
    state, setter = (
        Parser.head("int", Regex.digits().one_or_more())
        .value()
        .transform(int)
        .arg(lambda _, v: Int(v))
    ).prefix("a")("a123")
    assert state == State()
    assert setter(Int(0)) == Int(123)


def test_suffix():
    state, setter = (
        Parser.head("int", Regex.digits().one_or_more())
        .value()
        .transform(int)
        .arg(lambda _, v: Int(v))
        .suffix("a")("123a")
    )
    assert state == State()
    assert setter(Int(0)) == Int(123)
