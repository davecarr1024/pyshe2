from pysh.core.parser import Parser, State
from pysh.core.regex import Regex


def test_apply():
    assert Parser.head("int", Regex.digits().one_or_more()).value().transform(int)(
        "123"
    ) == (State(), 123)
