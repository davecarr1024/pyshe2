from pysh.core.parser import Parser, Suffix, State


def test_combine(subtests):
    for value in list[Parser](
        [
            Parser.head("a").suffix("b"),
            Parser.head("a") & "b",
        ]
    ):
        with subtests.test(value=value):
            assert value == Suffix(Parser.head("a"), Parser.head("b"))


def test_apply():
    assert Parser.head("a").value().suffix("b")("ab") == (State(), "a")
