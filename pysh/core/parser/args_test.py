from typing import Optional, Sequence

import pytest
from pysh.core import regex
from pysh.core.chars import Position
from pysh.core.parser import Arg, Args, Parser, State
from pysh.core.tokens import Token


def test_combine(subtests):
    a: Arg = Parser.head("a").arg("a")
    b: Arg = Parser.head("b").arg("b")
    c: Arg = Parser.head("c").arg("c")
    d: Arg = Parser.head("d").arg("d")
    for parser in list[Args](
        [
            a & b & c & d,
            (a & b) & c & d,
            a & (b & c) & d,
            a & b & (c & d),
            (a & b) & (c & d),
        ]
    ):
        with subtests.test(parser=parser):
            assert parser == Args.for_children(a, b, c, d)
