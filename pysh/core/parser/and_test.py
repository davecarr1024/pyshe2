from pysh.core.parser import And, Parser


def test_combine(subtests):
    a = Parser.head("a")
    b = Parser.head("b")
    c = Parser.head("c")
    d = Parser.head("d")
    for parser in list[And](
        [
            a & b & c & d,
            (a & b) & c & d,
            a & (b & c) & d,
            a & b & (c & d),
            (a & b) & (c & d),
        ]
    ):
        with subtests.test(parser=parser):
            assert parser == And.for_children(a, b, c, d)
