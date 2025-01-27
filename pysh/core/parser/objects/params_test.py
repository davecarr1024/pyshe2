from pysh.core import regex
from pysh.core.parser import Parser, State
from pysh.core.parser.objects import Arg, Param, Params

_int = Parser.head("int", regex.Regex.digits().one_or_more()).value().transform(int)


def test_combine(subtests):
    a: Param[int] = _int.param("a")
    b: Param[int] = _int.param("b")
    c: Param[int] = _int.param("c")
    d: Param[int] = _int.param("d")
    for params in list[Params](
        [
            a & b & c & d,
            (a & b) & c & d,
            a & (b & c) & d,
            a & b & (c & d),
            (a & b) & (c & d),
        ]
    ):
        with subtests.test(params=params):
            assert params == Params.for_children(a, b, c, d), params


def test_apply():
    assert (_int.param("a") & _int.param("b")).ignore_whitespace()("123 456") == (
        State(),
        [
            Arg[int]("a", 123),
            Arg[int]("b", 456),
        ],
    )
