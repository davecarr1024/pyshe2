from pysh.core.errors.error import Error


def test_eq(subtests):
    for lhs, rhs in list[tuple[Error, Error]](
        [
            (Error(), Error()),
            (
                Error(msg="a"),
                Error(msg="a"),
            ),
            (
                Error(
                    msg="a",
                    children=[
                        Error(msg="b"),
                    ],
                ),
                Error(
                    msg="a",
                    children=[
                        Error(msg="b"),
                    ],
                ),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs):
            assert lhs == rhs


def test_neq(subtests):
    for lhs, rhs in list[tuple[Error, Error]](
        [
            (Error(), Error(msg="a")),
            (
                Error(msg="a"),
                Error(msg="b"),
            ),
            (
                Error(
                    msg="a",
                    children=[
                        Error(msg="b"),
                    ],
                ),
                Error(
                    msg="a",
                    children=[
                        Error(msg="c"),
                    ],
                ),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs):
            assert lhs != rhs


def test_str(subtests):
    for error, expected in list[tuple[Error, str]](
        [
            (
                Error(msg="a"),
                "a",
            ),
            (
                Error(
                    msg="a",
                    children=[
                        Error(msg="b"),
                    ],
                ),
                "a\n  b",
            ),
        ]
    ):
        with subtests.test(error=error, expected=expected):
            assert str(error) == expected
