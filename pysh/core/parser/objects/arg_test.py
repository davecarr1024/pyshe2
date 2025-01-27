from pysh.core.parser.objects.arg import Arg


def test_as_dict():
    assert Arg[int]("a", 1).as_dict() == {"a": 1}
