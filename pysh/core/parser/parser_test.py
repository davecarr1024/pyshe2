from pysh.core.parser import Parser, State


def test_prefix():
    assert ("a" & Parser.head("b").value())("ab") == (State(), "b")


def test_suffix():
    assert (Parser.head("a").value() & "b")("ab") == (State(), "a")
