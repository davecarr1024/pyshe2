from pysh.core.chars import Position
from pysh.core.lexer import Lexer, Rule
from pysh.core.parser import Head, Parser, State
from pysh.core.regex import Regex
from pysh.core.tokens import Token


def test_prefix(subtests):
    for prefix in list[str | Rule](
        [
            "a",
            Rule.for_str("a"),
        ]
    ):
        with subtests.test(prefix=prefix):
            assert (prefix & Parser.head("b").value())("ab") == (State(), "b")


def test_suffix(subtests):
    for suffix in list[str | Rule](
        [
            "b",
            Rule.for_str("b"),
        ]
    ):
        with subtests.test(suffix=suffix):
            assert (Parser.head("a").value() & suffix)("ab") == (State(), "a")


def test_str(subtests):
    for input, expected in list[tuple[Parser, str]](
        [
            (Parser.head("a"), "a"),
            ("b" & Parser.head("a"), "b & a"),
            (Parser.head("a") & "b", "a & b"),
        ]
    ):
        with subtests.test(input=input, expected=expected):
            assert str(input) == expected


def test_with_lexer():
    assert Parser.head("a").value().with_lexer(Rule.for_str("b"))("ab") == (
        State.for_tokens(Token("b", "b", Position(0, 1))),
        "a",
    )


def test_ignore_whitespace():
    assert Parser.head("a").value().ignore_whitespace()(" a ") == (State(), "a")


def test_head(subtests):
    for head in list[Head](
        [
            Parser.head("a"),
            Parser.head("a", "a"),
            Parser.head("a", Regex.literal("a")),
            Parser.head(Rule.for_str("a")),
        ]
    ):
        with subtests.test(head=head):
            assert head == Head(Rule.for_str("a"))
