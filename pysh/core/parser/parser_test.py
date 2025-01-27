from pysh.core.chars import Position
from pysh.core.lexer import Lexer, Rule
from pysh.core.parser import Parser, State
from pysh.core.tokens import Token


def test_prefix():
    assert ("a" & Parser.head("b").value())("ab") == (State(), "b")


def test_suffix():
    assert (Parser.head("a").value() & "b")("ab") == (State(), "a")


def test_with_lexer():
    assert Parser.head("a").value().with_lexer(Lexer.for_rules(Rule.for_str("b")))(
        "ab"
    ) == (State.for_tokens(Token("b", "b", Position(0, 1))), "a")


def test_ignore_whitespace():
    assert Parser.head("a").value().ignore_whitespace()(" a ") == (State(), "a")
