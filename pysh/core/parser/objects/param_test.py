from pysh.core.lexer import Rule
from pysh.core.parser import Parser, State
from pysh.core.parser.objects import Param, Params, Arg
from pysh.core.regex import Regex

_int: Parser[int] = (
    Parser.head("int", Regex.digits().one_or_more()).value().transform(int)
)


def test_apply():
    assert _int.param("i")("123") == (State(), Arg[int]("i", 123))


def test_prefix(subtests):
    for prefix in list[str | Rule](
        [
            "a",
            Rule.for_str("a"),
        ]
    ):
        with subtests.test(prefix=prefix):
            assert (prefix & _int.param("i"))("a123") == (State(), Arg[int]("i", 123))


def test_suffix(subtests):
    for suffix in list[str | Rule](
        [
            "a",
            Rule.for_str("a"),
        ]
    ):
        with subtests.test(suffix=suffix):
            assert (_int.param("i") & suffix)("123a") == (State(), Arg[int]("i", 123))


def test_combine():
    a = _int.param("a")
    b = _int.param("b")
    assert a & b == Params.for_children(a, b)
    assert "z" & a == Param[int](_int, "a", _prefix=Parser.head("z"))
    assert a & "z" == Param[int](_int, "a", _suffix=Parser.head("z"))
