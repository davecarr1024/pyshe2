from pysh.core.parser import Parser, Prefix, State


def test_combine(subtests):
    for value in list[Parser](
        [
            Parser.head("b").prefix("a"),
            "a" & Parser.head("b"),
        ]
    ):
        with subtests.test(value=value):
            assert value == Prefix(Parser.head("b"), Parser.head("a"))


def test_apply():
    assert Parser.head("b").value().prefix("a")("ab") == (State(), "b")
