from pysh.core import regex
from pysh.core.parser import Parser
from pysh.core.parser.objects import Param, Params

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
            assert params == Params.for_children(a, b, c, d), str(
                (str(params), type(params))
            )
