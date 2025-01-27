from pysh.core.parser import Parser, State
from pysh.core.parser.objects.arg import Arg
from pysh.core.parser.objects.param import Param
from pysh.core.regex import Regex


def test_apply():
    assert Parser.head("int", Regex.digits().one_or_more()).value().transform(
        int
    ).param("a")("123") == (State(), Arg[int]("a", 123))
