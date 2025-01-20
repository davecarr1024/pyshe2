from dataclasses import dataclass
from re import L
from typing import Iterable

import pytest

from pysh.core.streams import Stream


@dataclass(frozen=True)
class _TestStream(Stream[int]): ...


def test_eq(subtests):
    for lhs, rhs in list[tuple[_TestStream, _TestStream]](
        [
            (
                _TestStream(),
                _TestStream(),
            ),
            (
                _TestStream([1, 2, 3]),
                _TestStream([1, 2, 3]),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs):
            assert lhs == rhs


def test_neq(subtests):
    for lhs, rhs in list[tuple[_TestStream, _TestStream]](
        [
            (
                _TestStream(),
                _TestStream([1]),
            ),
            (
                _TestStream([1]),
                _TestStream([2]),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs):
            assert lhs != rhs


def test_empty():
    assert _TestStream().empty()
    assert not _TestStream([1]).empty()


def test_head():
    pytest.raises(_TestStream.Error, _TestStream().head)
    assert 1 == _TestStream([1]).head()
    assert 1 == _TestStream([1, 2]).head()


def test_tail():
    pytest.raises(_TestStream.Error, _TestStream().tail)
    assert _TestStream([1]).tail() == _TestStream()
    assert _TestStream([1, 2]).tail() == _TestStream([2])


def test_add(subtests):
    for lhs, rhs, expected in list[tuple[_TestStream, _TestStream | int, _TestStream]](
        [
            (
                _TestStream(),
                _TestStream(),
                _TestStream(),
            ),
            (
                _TestStream(),
                _TestStream([1]),
                _TestStream([1]),
            ),
            (
                _TestStream([1]),
                _TestStream(),
                _TestStream([1]),
            ),
            (
                _TestStream([1]),
                _TestStream([2]),
                _TestStream([1, 2]),
            ),
            (
                _TestStream(),
                1,
                _TestStream([1]),
            ),
            (
                _TestStream([1]),
                2,
                _TestStream([1, 2]),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs):
            assert lhs + rhs == expected


def test_radd(subtests):
    for lhs, rhs, expected in list[tuple[int, _TestStream, _TestStream]](
        [
            (
                1,
                _TestStream(),
                _TestStream([1]),
            ),
            (
                1,
                _TestStream([2]),
                _TestStream([1, 2]),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs + rhs == expected


def test_for_values(subtests):
    for values, expected in list[tuple[Iterable[int], _TestStream]](
        [
            (
                [],
                _TestStream(),
            ),
            (
                [1],
                _TestStream([1]),
            ),
            (
                [1, 2],
                _TestStream([1, 2]),
            ),
        ]
    ):
        with subtests.test(values=values, expected=expected):
            assert _TestStream.for_values(*values) == expected
