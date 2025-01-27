from pysh.core.parser import Parser, State
from pysh.core.parser.objects import Param, Params, Arg
from pysh.core.regex import Regex

_int: Parser[int] = (
    Parser.head("int", Regex.digits().one_or_more()).value().transform(int)
)


def test_apply():
    assert _int.param("i")("123") == (State(), Arg[int]("i", 123))


def test_affix():
    assert ("a" & _int.param("i") & "b")("a123b") == (State(), Arg[int]("i", 123))


def test_combine():
    a = _int.param("a")
    b = _int.param("b")
    assert a & b == Params.for_children(a, b)
    assert "z" & a == Param[int](_int, "a", _prefix=Parser.head("z"))
    assert a & "z" == Param[int](_int, "a", _suffix=Parser.head("z"))
